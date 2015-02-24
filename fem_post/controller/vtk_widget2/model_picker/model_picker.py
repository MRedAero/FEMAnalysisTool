__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore

from ..vtk_globals import vtk_globals

from ..algorithms import GlobalIdFilter

from .no_picker import NoPicker
from .single_picker import SinglePicker
from .box_picker import BoxPicker

from .active_selections import ActiveSelections
from .selection_list import SelectionList


class ModelPicker(object):

    def __init__(self, parent, interactor_style):
        super(ModelPicker, self).__init__()

        self.parent = parent
        self.visible_filter = self.parent.visible_filter

        self.renderer = self.parent.renderer
        self.renderer_picked = self.parent.renderer_picked
        self.renderer_hovered = self.parent.renderer_hovered

        self.active_selections = ActiveSelections()
        self.active_selections.selection_changed.connect(self.active_selections_changed)

        self.hovered_selection = SelectionList()
        self.hovered_selection.selection_changed.connect(self.update_hovered_selection_data)

        self.picked_selection = SelectionList()
        self.picked_selection.selection_changed.connect(self.update_picked_selection_data)
        self.picked_selection.selection_changed.connect(self.update_ui_selection)
        self.picked_filter = GlobalIdFilter()
        self.picked_filter.SetInputConnection(self.visible_filter.all_port())

        self.interactor_style = None

        self.selection_type = 0
        self.set_selection_type(vtk_globals.SELECTION_SINGLE)

        self.no_picker = NoPicker(self)
        self.single_picker = SinglePicker(self)
        self.box_picker = BoxPicker(self)

        pick_list = self.parent.main_pipeline.node_actor
        self.single_picker.node_picker.AddPickList(pick_list)

        pick_list = self.parent.main_pipeline.vertex_actor
        self.single_picker.vertex_picker.AddPickList(pick_list)

        self.set_interactor_style(interactor_style)

    def reset_hovered_data(self, do_not_render=False):
        self.parent.hovered_pipeline.reset_data()

        if not do_not_render:
            self.render()

    def reset_picked_data(self, do_not_render=False):
        self.parent.selected_pipeline.reset_data()

        if not do_not_render:
            self.render()

    def update_hovered_selection_data(self):
        self.parent.hovered_pipeline.update_data(self.hovered_selection, self.single_picker.pick_type)

    def update_picked_selection_data(self):
        self.parent.selected_pipeline.update_data(self.picked_selection)

    def update_ui_selection(self):
        self.parent.update_ui_selection(self.picked_selection.to_string())

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
            if self.selection_type == -1:
                self.no_picker.connect_signals()
            elif self.selection_type == vtk_globals.SELECTION_SINGLE:
                self.single_picker.connect_signals()
            elif self.selection_type == vtk_globals.SELECTION_BOX:
                self.box_picker.connect_signals()
            elif self.selection_type == vtk_globals.SELECTION_POLY:
                self.poly_picker.connect_signals()

    def disconnect_interactor_style_signals(self):
        self.reset_hovered_data()
        if self.interactor_style is not None:
            if self.selection_type == -1:
                self.no_picker.disconnect_signals()
            elif self.selection_type == vtk_globals.SELECTION_SINGLE:
                self.single_picker.disconnect_signals()
            elif self.selection_type == vtk_globals.SELECTION_BOX:
                self.box_picker.disconnect_signals()
            elif self.selection_type == vtk_globals.SELECTION_POLY:
                self.poly_picker.disconnect_signals()

    def toggle_picking(self, entity_type, index):
        self.active_selections.toggle_picking(entity_type, index)

    def active_selections_changed(self):
        self.single_picker.set_picking(self.active_selections)
        #self.box_picker.set_picking(self.active_selections)

    def get_renderer(self):
        return self.renderer

    def get_renderer_picked(self):
        return self.renderer_picked

    def get_renderer_hovered(self):
        return self.renderer_hovered

    def render(self):
        self.parent.render()