__author__ = 'Michael Redmond'

from ..vtk_globals import vtk_globals

from .abstract_picker import AbstractPicker
from cell_picker import CellPicker
from vertex_picker import VertexPicker


class SinglePicker(AbstractPicker):
    def __init__(self, model_picker):
        super(SinglePicker, self).__init__(model_picker)

        self.nodes_active = True
        self.vertex_active = True

        self.node_picker = VertexPicker()
        self.node_picker.SetTolerance(0.006)

        self.vertex_picker = VertexPicker()
        self.vertex_picker.SetTolerance(0.006)

        self.cell_picker = CellPicker()
        self.cell_picker.SetTolerance(0.005)

        self._last_selection = None

        self._left_button_down = False
        self._ctrl_left_button_down = False
        self._right_button_down = False
        self._middle_button_down = False

        self._down_pos = None
        self._up_pos = None

        self.hovered_selection = None
        self.reset_hovered_selection()

        self.picked_selection = None
        self.reset_picked_selection()

        self.pick_type = None

    def reset_hovered_selection(self):
        self.hovered_selection = {'Node': [],
                          'Element': [],
                          'MPC': [],
                          'Load': [],
                          'Disp': []}

    def reset_picked_selection(self):
        self.picked_selection = {'Node': [],
                                  'Element': [],
                                  'MPC': [],
                                  'Load': [],
                                  'Disp': []}

    def set_data(self):

        data = self.model_picker.visible_filter.all_data()
        self.cell_picker.SetDataSet(data)

        if data.GetNumberOfCells() > 0:
            self.cell_picker.Update()

    def cell_pick(self, pos):

        if self.nodes_active:
            # try node pick
            self.node_picker.Pick(pos[0], pos[1], 0, self.model_picker.get_renderer())

            global_id = self.node_picker.GetCellGlobalId()

            if global_id != -1:
                self.pick_type = vtk_globals.VTK_NODE
                self._update_id(global_id)
                return True

        if self.vertex_active:
            # try vertex pick
            self.vertex_picker.Pick(pos[0], pos[1], 0, self.model_picker.get_renderer())

            global_id = self.vertex_picker.GetCellGlobalId()

            if global_id != -1:
                self.pick_type = vtk_globals.VTK_VERTEX
                self._update_id(global_id)

                #print self.vertex_picker.GetDataSet()

                return True

        # try cell pick
        data_set = self.cell_picker.GetDataSet()

        if self.model_picker.get_renderer() is None or data_set is None or \
                        data_set.GetNumberOfCells() == 0:
            return False

        self.cell_picker.Pick(pos[0], pos[1], 0, self.model_picker.get_renderer())

        _id = self.cell_picker.GetClosestCellId()

        if _id >= 0:

            global_id = self.cell_picker.GetClosestCellGlobalId()

            # any cell but vertex, doesn't matter
            self.pick_type = vtk_globals.VTK_QUAD

            self._update_id(global_id)

            return True

        self.pick_type = -1

        return False

    def _update_id(self, global_id):
        cell_type = vtk_globals.cell_type(global_id)

        selection = '%s %s' % (cell_type, str(global_id))

        if self._last_selection == selection:
            return

        self._last_selection = selection

        self.reset_hovered_selection()

        self.hovered_selection[cell_type] = [global_id]

        self.model_picker.hovered_selection.update_selection(self.hovered_selection)

    def mouse_move(self, obj, event, interactor, action):

        should_pick = True

        if self._left_button_down or self._ctrl_left_button_down or self._middle_button_down or self._right_button_down:
            self.reset_hovered_and_picked_data()
            should_pick = False

        action()

        if not should_pick:
            return

        pos = interactor.GetEventPosition()

        if not self.cell_pick(pos):
            self.reset_hovered_data()

    def reset_hovered_data(self):
        self._last_selection = None
        self.model_picker.reset_hovered_data()

    def reset_hovered_and_picked_data(self):
        self.reset_hovered_data()
        self.model_picker.reset_picked_data()

    def try_pick(self):
        if self._down_pos == self._up_pos:
            self.something_picked()
        else:
            self.model_picker.update_picked_selection_data()

    def left_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._left_button_down = True
        self._down_pos = interactor.GetEventPosition()

    def left_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._left_button_down = False
        self._up_pos = interactor.GetEventPosition()

        if picking_is_active:
            self.try_pick()
        else:
            self.model_picker.update_picked_selection_data()

    def ctrl_left_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._ctrl_left_button_down = True
        self._down_pos = interactor.GetEventPosition()

    def ctrl_left_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._ctrl_left_button_down = False
        self._up_pos = interactor.GetEventPosition()

        if picking_is_active:
            self.try_pick()
        else:
            self.model_picker.update_picked_selection_data()

    def left_button_double_click(self, obj, event, interactor, action):
        pass

    def middle_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._middle_button_down = True
        self._down_pos = interactor.GetEventPosition()

    def middle_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._middle_button_down = False
        self._up_pos = interactor.GetEventPosition()

        if picking_is_active:
            self.try_pick()
        else:
            self.model_picker.update_picked_selection_data()

    def right_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._right_button_down = True
        self._down_pos = interactor.GetEventPosition()

    def right_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._right_button_down = False
        self._up_pos = interactor.GetEventPosition()

        if picking_is_active:
            self.try_pick()
        else:
            self.model_picker.update_picked_selection_data()

    def mouse_wheel_forward(self, obj, event, interactor, action):
        self.reset_hovered_and_picked_data()
        action()
        self.model_picker.update_picked_selection_data()

    def mouse_wheel_backward(self, obj, event, interactor, action):
        self.reset_hovered_and_picked_data()
        action()
        self.model_picker.update_picked_selection_data()

    def set_picking(self, active_selections):

        self.nodes_active = active_selections.nodes
        self.vertex_active = active_selections.points

        self.cell_picker.set_picking(vtk_globals.VTK_NODE, False)
        self.cell_picker.set_picking(vtk_globals.VTK_VERTEX, False)
        self.cell_picker.set_picking(vtk_globals.VTK_LINE, active_selections.bars)
        self.cell_picker.set_picking(vtk_globals.VTK_TRI, active_selections.tris)
        self.cell_picker.set_picking(vtk_globals.VTK_QUAD, active_selections.quads)
        self.cell_picker.set_picking(vtk_globals.VTK_POLY_LINE, active_selections.mpcs)

    def something_picked(self):
        self.reset_picked_selection()

        if self._last_selection is not None:
            tmp = self._last_selection.split(' ')
            self.picked_selection[tmp[0]] = int(round(float(tmp[1]), 0))

        self.model_picker.picked_selection.update_selection(self.picked_selection)