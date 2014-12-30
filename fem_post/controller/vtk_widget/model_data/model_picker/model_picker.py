__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore

from ...vtk_globals import *
from ...custom_pickers import *

from .data_extractor import DataExtractor
from .active_selections import ActiveSelections

from .single_picker import SinglePicker
from .box_picker import BoxPicker
from .poly_picker import PolyPicker


class ModelPicker(object):
    def __init__(self):
        super(ModelPicker, self).__init__()

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
        self.selected_actor.GetProperty().SetColor(0., 0.5, 0.5)
        self.selected_actor.GetProperty().SetEdgeColor(0., 0.5, 0.5)
        self.selected_actor.GetProperty().SetLineWidth(3)
        self.selected_actor.GetProperty().SetPointSize(6)

        self.hover_actor.SetMapper(self.hover_mapper)
        self.selected_actor.SetMapper(self.selected_mapper)

        self.selection_option = SELECTION_REPLACE

        self.active_selections = ActiveSelections()
        self.active_selections.selection_changed.connect(self.active_selections_changed)

        self.selection_type = 0

        self.set_selection_type(SELECTION_SINGLE)

        self.interactor_style = None

        self.single_picker = SinglePicker(self)
        self.box_picker = BoxPicker(self)
        self.poly_picker = PolyPicker(self)

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

        print 'active selections changed'

    def toggle_picking(self, entity_type, index):
        self.active_selections.toggle_picking(entity_type, index)

    def render(self):
        self.interactor_style.GetInteractor().GetRenderWindow().Render()