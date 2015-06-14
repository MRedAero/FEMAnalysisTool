__author__ = 'Michael Redmond'

import vtk

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from base_app.simple_pubsub import pub
from base_app.utilities import BaseObject

from fem_post.application.vtk_widget import vtk_globals
from fem_post.application.vtk_widget.algorithms import (BDFDataSource, VisibleFilter, GroupFilter)
from .master_pipeline import MasterPipeline
from fem_post.application.vtk_widget.widgets import CoordinateAxes

from vtk_extensions.interactor import vtkDefaultInteractorStyle

from .vtk_base_widget import VTKBaseWidget

from .model_picker import ModelPicker

from .vtk_view import VTKView


class VTKWidget(VTKBaseWidget):
    def __init__(self, main_window):
        super(VTKWidget, self).__init__(main_window)

        self._vtk_view = VTKView(self)
        self._model_picker = ModelPicker(self)
        self._master_pipeline = MasterPipeline(self)

        self.interactor = self._vtk_view.get_interactor()
        self._main_window.layout().addWidget(self.interactor)
        self.iren = self.interactor.GetRenderWindow().GetInteractor()

        self.axes = CoordinateAxes(self.interactor)

        self.interactor_style = vtkDefaultInteractorStyle()
        self.interactor_style.AddObserver(vtk.vtkCommand.EndPickEvent, self._pick_event)

        self.interactor_style.set_default_renderer(self._vtk_view.get_renderers()[0])

        self.interactor.SetInteractorStyle(self.interactor_style)

        self.interactor.Start()

        self._master_pipeline.visible_filter.add_callback(self.interactor_style.model_picker.set_data)

        self.interactor_style.set_button_actions(self._actions, self._picking)

        self.show_hide = False
        self.show = True

        self.bdf = None

    def get_renderers(self):
        return self._vtk_view.get_renderers()

    def _pick_event(self, obj, event):
        event_data = self.interactor_style.get_pick_event_data()
        self._model_picker.pick(event_data)

    def set_file(self, file):
        self._master_pipeline.set_file(file)

    def get_parent(self):
        return self._main_window

    def initialize(self):
        self.iren.Initialize()

    def render(self):
        self.interactor.GetRenderWindow().Render()

    def toggle_picking(self, entity_type, index=None):
        self.interactor_style.model_picker.toggle_picking(entity_type, index)

    def update_ui_selection(self, selection):
        pub.publish("vtk.set_selection_box", selection)

    def replace_selection_button(self):
        self.interactor_style.model_picker.picked_selection.selection_type = vtk_globals.SELECTION_REPLACE

    def append_selection_button(self):
        self.interactor_style.model_picker.picked_selection.selection_type = vtk_globals.SELECTION_APPEND

    def remove_selection_button(self):
        self.interactor_style.model_picker.picked_selection.selection_type = vtk_globals.SELECTION_REMOVE

    def single_pick_button(self):
        self.interactor_style.set_selection_type(vtk_globals.SELECTION_SINGLE)

    def box_pick_button(self):
        self.interactor_style.set_selection_type(vtk_globals.SELECTION_BOX)

    def poly_pick_button(self):
        self.interactor_style.set_selection_type(vtk_globals.SELECTION_POLY)

    def unload(self):
        # this is required so that the vtk widget will release its memory

        self._main_window.layout().removeWidget(self.interactor)
        self.interactor.Finalize()
        self._main_window = None