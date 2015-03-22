__author__ = 'Michael Redmond'

from ...vtk_globals import vtk_globals
from ...algorithms import GlobalIdFilter

from .no_picker import NoPicker
from .single_picker import SinglePicker
from .box_picker import BoxPicker
from .poly_picker import PolyPicker

from .active_selections import ActiveSelections
from .selection_list import SelectionList


class ModelPicker(object):

    def __init__(self, vtk_widget, interactor_style):
        super(ModelPicker, self).__init__()

        self.vtk_widget = vtk_widget
        self.visible_filter = self.vtk_widget.visible_filter

        self.renderer = self.vtk_widget.renderer
        self.renderer_picked = self.vtk_widget.renderer_picked
        self.renderer_hovered = self.vtk_widget.renderer_hovered

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
        self.poly_picker = PolyPicker(self)

        pick_list = self.vtk_widget.main_pipeline.node_actor
        self.single_picker.node_picker.AddPickList(pick_list)

        pick_list = self.vtk_widget.main_pipeline.vertex_actor
        self.single_picker.vertex_picker.AddPickList(pick_list)

        self.set_interactor_style(interactor_style)

    def set_data(self):
        self.single_picker.set_data()
        self.box_picker.set_data()

    def reset_hovered_data(self, do_not_render=False):
        self.vtk_widget.hovered_pipeline.reset_data()

        if not do_not_render:
            self.render()

    def reset_picked_data(self, do_not_render=False):
        self.vtk_widget.selected_pipeline.reset_data()

        if not do_not_render:
            self.render()

    def update_hovered_selection_data(self):
        self.vtk_widget.hovered_pipeline.update_data(self.hovered_selection, self.single_picker.pick_type)

    def update_picked_selection_data(self):
        self.vtk_widget.selected_pipeline.update_data(self.picked_selection)

    def update_ui_selection(self):
        self.vtk_widget.update_ui_selection(self.picked_selection.to_string())

    def set_interactor_style(self, interactor_style):
        self.interactor_style = interactor_style

        self.connect_interactor_style_signals()

    def set_selection_type(self, value):
        if value == self.selection_type:
            return

        self.selection_type = value

        self.connect_interactor_style_signals()

    def connect_interactor_style_signals(self):
        if self.interactor_style is not None:
            if self.selection_type == -1:
                self.interactor_style.active_picker = self.no_picker
            elif self.selection_type == vtk_globals.SELECTION_SINGLE:
                self.interactor_style.active_picker = self.single_picker
            elif self.selection_type == vtk_globals.SELECTION_BOX:
                self.interactor_style.active_picker = self.box_picker
            elif self.selection_type == vtk_globals.SELECTION_POLY:
                self.interactor_style.active_picker = self.poly_picker

        self.reset_hovered_data()

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
        self.vtk_widget.render()