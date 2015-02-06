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

        self.hover_data = vtk.vtkPolyData()
        self.selected_data = vtk.vtkPolyData()

        #################### test #####################
        self.selected_elements = vtk.vtkUnstructuredGrid()
        self.selected_nodes = vtk.vtkUnstructuredGrid()

        self.selected_elements_mapper = vtk.vtkPolyDataMapper2D()
        self.selected_nodes_mapper = vtk.vtkPolyDataMapper2D()

        self.coordinate = vtk.vtkCoordinate()
        self.coordinate.SetCoordinateSystem(5)

        self.selected_elements_mapper.SetTransformCoordinate(self.coordinate)
        self.selected_nodes_mapper.SetTransformCoordinate(self.coordinate)

        self.selected_elements_geometry_filter = vtk.vtkGeometryFilter()
        self.selected_nodes_geometry_filter = vtk.vtkGeometryFilter()

        self.selected_elements_edges = vtk.vtkExtractEdges()
        self.selected_nodes_edges = vtk.vtkExtractEdges()

        #################### test #####################

        self.hover_mapper = vtk.vtkPolyDataMapper()
        self.selected_mapper = vtk.vtkPolyDataMapper()

        if VTK_VERSION >= 6.0:
            self.hover_mapper.SetInputData(self.hover_data)
            self.selected_mapper.SetInputData(self.selected_data)

            #################### test #####################
            #self.selected_elements_object_filter.SetInputData(self.selected_elements)
            #self.selected_nodes_object_filter.SetInputData(self.selected_nodes)

            self.selected_elements_geometry_filter.SetInputData(self.selected_elements)
            self.selected_nodes_geometry_filter.SetInputData(self.selected_nodes)

            self.selected_elements_geometry_filter.Update()
            self.selected_nodes_geometry_filter.Update()

            #self.selected_elements_object_filter.Update()
            #self.selected_nodes_object_filter.Update()

            #self.selected_elements_mapper.SetInputDataObject(self.selected_elements_object_filter.GetOutput())
            #self.selected_nodes_mapper.SetInputDataObject(self.selected_nodes_object_filter.GetOutput())

            self.selected_elements_edges.SetInputData(self.selected_elements_geometry_filter.GetOutput())
            self.selected_nodes_edges.SetInputData(self.selected_nodes_geometry_filter.GetOutput())

            self.selected_elements_edges.Update()
            self.selected_nodes_edges.Update()

            self.selected_elements_mapper.SetInputData(self.selected_elements_edges.GetOutput())
            self.selected_nodes_mapper.SetInputData(self.selected_nodes_edges.GetOutput())

            #################### test #####################

        else:
            self.hover_mapper.SetInput(self.hover_data)
            self.selected_mapper.SetInput(self.selected_data)

            #################### test #####################
            self.selected_elements_object_filter.SetInput(self.selected_elements)
            self.selected_nodes_object_filter.SetInput(self.selected_nodes)

            self.selected_elements_mapper.SetInputDataObject(self.selected_elements_object_filter.GetOutput())
            self.selected_nodes_mapper.SetInputDataObject(self.selected_nodes_object_filter.GetOutput())
            #################### test #####################

        self.hover_actor = vtk.vtkActor()
        self.selected_actor = vtk.vtkActor()

        #################### test #####################
        self.selected_elements_actor = vtk.vtkActor2D()
        self.selected_nodes_actor = vtk.vtkActor2D()
        #################### test #####################

        self.hover_actor.GetProperty().EdgeVisibilityOn()
        self.hover_actor.GetProperty().SetColor(0.5, 0.5, 0)
        self.hover_actor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
        self.hover_actor.GetProperty().SetLineWidth(3)
        self.hover_actor.GetProperty().SetOpacity(0.5)
        self.hover_actor.GetProperty().SetPointSize(6)

        self.selected_actor.GetProperty().EdgeVisibilityOn()
        self.selected_actor.GetProperty().SetColor(0., 0.5, 0.5)
        self.selected_actor.GetProperty().SetEdgeColor(0., 0.5, 0.5)
        self.selected_actor.GetProperty().SetLineWidth(1)
        #self.selected_actor.GetProperty().SetPointSize(6)
        self.selected_actor.GetProperty().SetRepresentationToWireframe()

        #################### test #####################
#        self.selected_elements_actor.GetProperty().EdgeVisibilityOn()
        self.selected_elements_actor.GetProperty().SetColor(0., 0.5, 0.5)
#        self.selected_elements_actor.GetProperty().SetEdgeColor(0., 0.5, 0.5)
        self.selected_elements_actor.GetProperty().SetLineWidth(2)
        #self.selected_elements_actor.GetProperty().SetPointSize(6)
        #self.selected_elements_actor.GetProperty().SetRepresentationToWireframe()

        #self.selected_nodes_actor.GetProperty().EdgeVisibilityOn()
        self.selected_nodes_actor.GetProperty().SetColor(0., 0.5, 0.5)
        #self.selected_nodes_actor.GetProperty().SetEdgeColor(0., 0.5, 0.5)
        self.selected_nodes_actor.GetProperty().SetLineWidth(2)
        #self.selected_nodes_actor.GetProperty().SetPointSize(6)
        #self.selected_nodes_actor.GetProperty().SetRepresentationToWireframe()
        #################### test #####################

        self.hover_actor.SetMapper(self.hover_mapper)
        self.selected_actor.SetMapper(self.selected_mapper)

        #################### test #####################
        self.selected_elements_actor.SetMapper(self.selected_elements_mapper)
        self.selected_nodes_actor.SetMapper(self.selected_nodes_mapper)
        #################### test #####################

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

            #################### test #####################
            self.pipeline.get_renderer().RemoveActor(self.selected_elements_actor)
            self.pipeline.get_renderer().RemoveActor(self.selected_nodes_actor)
            #################### test #####################

        self.pipeline = pipeline
        """:type: fem_post.controller.vtk_widget.pipelines.DataPipeline"""

        self.pipeline.data_updated.connect(self.update_data)
        self.pipeline.get_renderer().AddActor(self.hover_actor)
        self.pipeline.get_renderer().AddActor(self.selected_actor)

        #################### test #####################
        self.pipeline.get_renderer().AddActor2D(self.selected_elements_actor)
        self.pipeline.get_renderer().AddActor2D(self.selected_nodes_actor)
        #################### test #####################

        self.single_picker.node_picker.Renderer = self.get_renderer()

        self.update_data()

    def update_data(self):
        if self.pipeline is None:
            return

        self.single_picker.set_data()
        self.box_picker.set_data()

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

        #################### test #####################
        self.selected_elements.Reset()
        self.selected_nodes.Reset()
        #################### test #####################

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
        self.box_picker.set_picking(self.active_selections)

    def reset_selected_data(self, do_not_render=False):
        self.selected_data.Reset()
        self.selected_data.Modified()

        #################### test #####################
        self.selected_elements.Reset()
        self.selected_elements.GetCellData().Reset()
        self.selected_elements.Modified()
        self.selected_nodes.Reset()
        self.selected_nodes.GetCellData().Reset()
        self.selected_nodes.Modified()

        self.selected_elements_geometry_filter.Update()
        self.selected_nodes_geometry_filter.Update()

        self.selected_elements_edges.Update()
        self.selected_nodes_edges.Update()

        #################### test #####################

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

        #return

        self.selected_data.Reset()

        #################### test #####################
        self.selected_elements.Reset()
        self.selected_elements.GetCellData().Reset()
        self.selected_nodes.Reset()
        self.selected_nodes.GetCellData().Reset()
        #################### test #####################

        data = self.get_data()

        node_data = data['nodes']
        element_data = data['elements']

        self.node_filter.set_selection_list(self.selection_list.nodes, True)
        self.node_filter.set_input_data(node_data)

        self.element_filter.set_selection_list(self.selection_list.elements, True)
        self.element_filter.set_input_data(element_data)

        selected_nodes = self.node_filter.selected_data()
        self.selected_nodes.ShallowCopy(selected_nodes)

        selected_elements = self.element_filter.selected_data()
        self.selected_elements.ShallowCopy(selected_elements)

        self.selected_elements.Modified()
        self.selected_nodes.Modified()

        self.selected_elements_geometry_filter.Update()
        self.selected_nodes_geometry_filter.Update()

        self.selected_elements_edges.Update()
        self.selected_nodes_edges.Update()

        #self.selected_elements_mapper.Modified()
        #self.selected_nodes_mapper.Modified()

        #print self.selected_elements_geometry_filter.GetOutput()

        self.render()

    def update_selection_data_old2(self):

        #return

        self.selected_data.Reset()

        #################### test #####################
        self.selected_elements.Reset()
        self.selected_elements.GetCellData().Reset()
        self.selected_nodes.Reset()
        self.selected_nodes.GetCellData().Reset()
        #################### test #####################

        data = self.get_data()

        node_data = data['nodes']
        element_data = data['elements']

        self.node_filter.set_selection_list(self.selection_list.nodes, True)
        self.node_filter.set_input_data(node_data)

        self.element_filter.set_selection_list(self.selection_list.elements, True)
        self.element_filter.set_input_data(element_data)

        renderer = self.get_renderer()

        selected_nodes = self.node_filter.selected_data()
        self.selected_nodes.ShallowCopy(selected_nodes)
        #self.selected_nodes.GetCellData().DeepCopy(selected_nodes.GetCellData())
        node_points = self.selected_nodes.GetPoints()

        if node_points is not None:
            for i in xrange(node_points.GetNumberOfPoints()):
                new_pos = project_point_from_screen(node_points.GetPoint(i), renderer, .001)
                node_points.SetPoint(i, new_pos[:3])

        selected_elements = self.element_filter.selected_data()
        self.selected_elements.ShallowCopy(selected_elements)
        #self.selected_elements.GetCellData().DeepCopy(selected_elements.GetCellData())
        element_points = self.selected_elements.GetPoints()

        if element_points is not None:
            for i in xrange(element_points.GetNumberOfPoints()):
                new_pos = project_point_from_screen(element_points.GetPoint(i), renderer, .001)
                element_points.SetPoint(i, new_pos[:3])

        self.selected_elements.Modified()
        self.selected_nodes.Modified()

        self.render()

        #for i in xrange(self.selection_list.mpcs):
        #    pass

        #for i in xrange(self.selection_list.loads):
        #    pass

        #for i in xrange(self.selection_list.disps):
        #    pass

    def update_selection_data_old(self):

        #return

        self.selected_data.Reset()

        data = self.get_data()

        node_data = data['nodes']
        element_data = data['elements']

        self.node_filter.set_selection_list(self.selection_list.nodes, True)
        self.node_filter.set_input_data(node_data)

        selected_nodes = self.node_filter.selected_data()
        node_points = selected_nodes.GetPoints()

        self.element_filter.set_selection_list(self.selection_list.elements, True)
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

            elif point_count == 3:

                cell = vtk.vtkTriangle()
                ids = cell.GetPointIds()

                for j in xrange(3):

                    pos = element_points.GetPoint(point_ids.GetId(j))
                    new_pos = project_point_from_screen(pos, renderer, .001)
                    selected_points.InsertNextPoint(new_pos[:3])

                    ids.SetId(j, id)
                    id += 1

                cell_array.InsertNextCell(cell)
                continue

            elif point_count == 4:

                cell = vtk.vtkQuad()
                ids = cell.GetPointIds()

                for j in xrange(4):

                    pos = element_points.GetPoint(point_ids.GetId(j))
                    new_pos = project_point_from_screen(pos, renderer, .001)
                    selected_points.InsertNextPoint(new_pos[:3])

                    ids.SetId(j, id)
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

        self.node_filter.set_selection_list(self.selection_list.nodes, True)
        self.node_filter.set_input_data(node_data)
        original_node_ids = self.node_filter.selected_data().GetCellData().GetArray("original_ids")

        self.element_filter.set_selection_list(self.selection_list.elements, True)
        self.element_filter.set_input_data(element_data)
        original_element_ids = self.element_filter.selected_data().GetCellData().GetArray("original_ids")

        original_data = self.pipeline.get_data()
        node_visible = original_data.nodes.GetCellData().GetArray("visible")
        element_visible = original_data.elements.GetCellData().GetArray("visible")

        for i in xrange(original_node_ids.GetNumberOfTuples()):
            id = int(original_node_ids.GetValue(i))
            previous_value = int(node_visible.GetTuple1(id))
            node_visible.SetTuple1(id, -previous_value)

        for i in xrange(original_element_ids.GetNumberOfTuples()):
            id = int(original_element_ids.GetValue(i))
            previous_value = int(element_visible.GetTuple1(id))
            element_visible.SetTuple1(id, -previous_value)

        self.pipeline.update()
        self.render()

    def render(self):
        self.interactor_style.GetInteractor().GetRenderWindow().Render()