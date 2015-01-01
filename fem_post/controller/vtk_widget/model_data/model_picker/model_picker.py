__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore

from ...vtk_globals import *
from ...custom_pickers import *

from .data_extractor import DataExtractor
from .active_selections import ActiveSelections
from .selection_list import SelectionList

from .single_picker import SinglePicker
from .box_picker import BoxPicker
from .poly_picker import PolyPicker

from ...filters import GlobalIdFilter


class ModelPicker(object):
    def __init__(self, vtk_widget):
        super(ModelPicker, self).__init__()

        self.vtk_widget = vtk_widget

        self.pipeline = None

        self.poly_points = vtk.vtkPoints()
        self.poly_line = vtk.vtkPolyLine()
        self.poly_data = vtk.vtkUnstructuredGrid()
        self.poly_plane = vtk.vtkPolyPlane()

        self.poly_data.SetPoints(self.poly_points)
        self.poly_data.InsertNextCell(self.poly_line.GetCellType(), self.poly_line.GetPointIds())
        self.poly_plane.SetPolyLine(self.poly_line)

        self.hover_data = vtk.vtkPolyData()
        self.selected_data = vtk.vtkPolyData()

        self.hover_mapper = vtk.vtkPolyDataMapper()
        self.selected_mapper = vtk.vtkPolyDataMapper()

        if VTK_VERSION >= 6.0:
            self.hover_mapper.SetInputData(self.hover_data)
            self.selected_mapper.SetInputData(self.selected_data)
        else:
            self.hover_mapper.SetInput(self.hover_data)
            self.selected_mapper.SetInput(self.selected_data)

        self.hover_actor = vtk.vtkActor()
        self.selected_actor = vtk.vtkActor()

        self.hover_actor.GetProperty().EdgeVisibilityOn()
        self.hover_actor.GetProperty().SetColor(0.5, 0.5, 0)
        self.hover_actor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
        self.hover_actor.GetProperty().SetLineWidth(3)
        self.hover_actor.GetProperty().SetOpacity(0.5)
        self.hover_actor.GetProperty().SetPointSize(6)

        self.selected_actor.GetProperty().EdgeVisibilityOn()
        #self.selected_actor.GetProperty().SetColor(0., 0.5, 0.5)
        self.selected_actor.GetProperty().SetEdgeColor(0., 0.5, 0.5)
        self.selected_actor.GetProperty().SetLineWidth(3)
        #self.selected_actor.GetProperty().SetPointSize(6)

        self.hover_actor.SetMapper(self.hover_mapper)
        self.selected_actor.SetMapper(self.selected_mapper)

        self.active_selections = ActiveSelections()
        self.active_selections.selection_changed.connect(self.active_selections_changed)

        self.selection_list = SelectionList()
        self.selection_list.selection_changed.connect(self.update_selection_data)
        self.selection_list.selection_changed.connect(self.update_ui_selection)

        self.selection_type = 0
        self.set_selection_type(SELECTION_SINGLE)

        self.interactor_style = None

        self.single_picker = SinglePicker(self)
        self.box_picker = BoxPicker(self)
        self.poly_picker = PolyPicker(self)

        self.node_filter = GlobalIdFilter()
        self.element_filter = GlobalIdFilter()

    def set_pipeline(self, pipeline):
        if self.pipeline is not None:
            self.pipeline.data_updated.disconnect(self.update_data)
            self.pipeline.get_renderer().RemoveActor(self.hover_actor)
            self.pipeline.get_renderer().RemoveActor(self.selected_actor)

        self.pipeline = pipeline
        """:type: fem_post.controller.vtk_widget.pipelines.DataPipeline"""

        self.pipeline.data_updated.connect(self.update_data)
        self.pipeline.get_renderer().AddActor(self.hover_actor)
        self.pipeline.get_renderer().AddActor(self.selected_actor)

        self.single_picker.node_picker.Renderer = self.get_renderer()

        self.update_data()

    def update_data(self):
        if self.pipeline is None:
            return

        self.single_picker.set_data()

    def get_data(self):
        return {'nodes': self.pipeline.node_mapper.GetInput(),
                'elements': self.pipeline.element_mapper.GetInput(),
                'rbes': self.pipeline.rbe_mapper.GetInput()}

    def get_actors(self):
        return {'nodes': self.pipeline.node_actor,
                'elements': self.pipeline.element_actor,
                'rbes': self.pipeline.rbe_actor}

    def get_renderer(self):
        if self.pipeline is None:
            return None

        return self.pipeline.get_renderer()

    def reset(self):
        self.poly_points.Reset()
        self.poly_line.Reset()

        self.hover_data.Reset()
        self.selected_data.Reset()

    def set_interactor_style(self, interactor_style):
        if self.interactor_style is not None:
            self.disconnect_interactor_style_signals()

        self.interactor_style = interactor_style

        self.connect_interactor_style_signals()

    def set_selection_type(self, value):
        if value == self.selection_type:
            return

        self.disconnect_interactor_style_signals()

        self.selection_type = value

        self.connect_interactor_style_signals()

    def connect_interactor_style_signals(self):
        if self.interactor_style is not None:
            if self.selection_type == SELECTION_SINGLE:
                self.single_picker.connect_signals()
            elif self.selection_type == SELECTION_BOX:
                self.box_picker.connect_signals()
            elif self.selection_type == SELECTION_POLY:
                self.poly_picker.connect_signals()

    def disconnect_interactor_style_signals(self):
        if self.interactor_style is not None:
            if self.selection_type == SELECTION_SINGLE:
                self.single_picker.disconnect_signals()
            elif self.selection_type == SELECTION_BOX:
                self.box_picker.disconnect_signals()
            elif self.selection_type == SELECTION_POLY:
                self.poly_picker.disconnect_signals()

    def active_selections_changed(self):
        self.single_picker.set_picking(self.active_selections)

    def reset_selected_data(self, do_not_render=False):
        self.selected_data.Reset()
        self.selected_data.Modified()

        if not do_not_render:
            self.render()

    def reset_hover_data(self, do_not_render=False):
        self.hover_data.Reset()
        self.hover_data.Modified()

        if not do_not_render:
            self.render()

    def reset_data(self, do_not_render=False):
        self.reset_selected_data(do_not_render)
        self.reset_hover_data(do_not_render)

    def update_selection_data(self):

        self.selected_data.Reset()

        data = self.get_data()

        node_data = data['nodes']
        element_data = data['elements']

        self.node_filter.set_global_id_selection(self.selection_list.nodes, True)
        self.node_filter.set_input_data(node_data)

        selected_nodes = self.node_filter.selected_data()
        node_points = selected_nodes.GetPoints()

        self.element_filter.set_global_id_selection(self.selection_list.elements, True)
        self.element_filter.set_input_data(element_data)

        selected_elements = self.element_filter.selected_data()
        element_points = selected_elements.GetPoints()

        selected_points = vtk.vtkPoints()

        renderer = self.get_renderer()

        id = 0

        cell_array = vtk.vtkCellArray()

        for i in xrange(selected_nodes.GetNumberOfCells()):
            point_ids = selected_nodes.GetCell(i).GetPointIds()

            pos = node_points.GetPoint(point_ids.GetId(0))

            new_pos = project_point_from_screen(pos, renderer, .001)
            selected_points.InsertNextPoint(new_pos[:3])

            cell = vtk.vtkVertex()
            ids = cell.GetPointIds()
            ids.SetId(0, id)
            id += 1

            cell_array.InsertNextCell(cell)

        for i in xrange(selected_elements.GetNumberOfCells()):

            point_ids = selected_elements.GetCell(i).GetPointIds()

            point_count = point_ids.GetNumberOfIds()

            if point_count == 1:
                pos = element_points.GetPoint(point_ids.GetId(0))

                new_pos = project_point_from_screen(pos, renderer, .001)
                selected_points.InsertNextPoint(new_pos[:3])

                cell = vtk.vtkVertex()
                ids = cell.GetPointIds()
                ids.SetId(0, id)
                id += 1

                cell_array.InsertNextCell(cell)
                continue

            elif point_count == 2:

                cell = vtk.vtkLine()
                ids = cell.GetPointIds()

                for j in xrange(2):

                    pos = element_points.GetPoint(point_ids.GetId(j))
                    new_pos = project_point_from_screen(pos, renderer, .001)
                    selected_points.InsertNextPoint(new_pos[:3])

                    ids.SetId(j, id)
                    id += 1

                cell_array.InsertNextCell(cell)
                continue

            elif point_count > 2:

                for j in xrange(1, point_count+1):

                    cell = vtk.vtkLine()
                    ids = cell.GetPointIds()

                    pos1 = element_points.GetPoint(point_ids.GetId(j-1))

                    if j == point_count:
                        pos2 = element_points.GetPoint(point_ids.GetId(0))
                    else:
                        pos2 = element_points.GetPoint(point_ids.GetId(j))

                    new_pos1 = project_point_from_screen(pos1, renderer, .001)
                    new_pos2 = project_point_from_screen(pos2, renderer, .001)

                    selected_points.InsertNextPoint(new_pos1[:3])
                    selected_points.InsertNextPoint(new_pos2[:3])

                    ids.SetId(0, id)
                    id += 1
                    ids.SetId(1, id)
                    id += 1

                    cell_array.InsertNextCell(cell)
                continue

        self.selected_data.SetPoints(selected_points)
        self.selected_data.SetVerts(cell_array)
        self.selected_data.SetLines(cell_array)
        self.selected_data.SetPolys(cell_array)
        self.selected_data.Modified()

        self.render()

        #for i in xrange(self.selection_list.mpcs):
        #    pass

        #for i in xrange(self.selection_list.loads):
        #    pass

        #for i in xrange(self.selection_list.disps):
        #    pass

    def update_ui_selection(self):
        self.vtk_widget.update_ui_selection(self.selection_list.to_string())

    def toggle_picking(self, entity_type, index):
        self.active_selections.toggle_picking(entity_type, index)

    def toggle_hidden(self):
        data = self.get_data()

        node_data = data['nodes']
        element_data = data['elements']

        self.node_filter.set_global_id_selection(self.selection_list.nodes, True)
        self.node_filter.set_input_data(node_data)
        selected_node_ids = self.node_filter.selected_data().GetCellData().GetArray("vtkOriginalCellIds")

        self.element_filter.set_global_id_selection(self.selection_list.elements, True)
        self.element_filter.set_input_data(element_data)
        selected_element_ids = self.element_filter.selected_data().GetCellData().GetArray("vtkOriginalCellIds")

        original_data = self.pipeline.get_data()
        node_visible = original_data.nodes.GetCellData().GetArray("visible")
        element_visible = original_data.elements.GetCellData().GetArray("visible")

        for i in xrange(selected_node_ids.GetNumberOfTuples()):
            id = int(selected_node_ids.GetValue(i))
            previous_value = int(node_visible.GetTuple1(id))
            node_visible.SetTuple1(id, -previous_value)

        for i in xrange(selected_element_ids.GetNumberOfTuples()):
            id = int(selected_element_ids.GetValue(i))
            print id
            previous_value = int(element_visible.GetTuple1(id))
            element_visible.SetTuple1(id, -previous_value)

        self.pipeline.update()
        self.render()

    def render(self):
        self.interactor_style.GetInteractor().GetRenderWindow().Render()