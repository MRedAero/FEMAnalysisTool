__author__ = 'Michael Redmond'

from .abstract_picker import AbstractPicker
from ...custom_pickers import *
from .active_selections import ActiveSelections
from ...vtk_globals import *


class SinglePicker(AbstractPicker):
    def __init__(self, model_picker):
        super(SinglePicker, self).__init__(model_picker)

        self.node_picker = vtkNodeCellPicker()
        self.element_picker = vtkThruCellPicker()
        self.rbe_picker = vtkThruCellPicker()

        self.node_picker.SetTolerance(0.005)
        self.element_picker.SetTolerance(0.005)
        self.rbe_picker.SetTolerance(0.005)

        self._last_selection = None

        self._left_button_down = False
        self._ctrl_left_button_down = False
        self._right_button_down = False
        self._middle_button_down = False

        self._down_pos = None
        self._up_pos = None

        self.selection = None
        self.reset_selection()

    def reset_selection(self):
        self.selection = {'nodes': [],
                          'elements': [],
                          'mpcs': [],
                          'loads': [],
                          'disps': []}

    def set_data(self):
        data = self.model_picker.get_data()

        node_actor = self.model_picker.get_actors()['nodes']

        self.node_picker.add_pick_list(node_actor)
        self.element_picker.SetDataSet(data['elements'])
        self.rbe_picker.SetDataSet(data['rbes'])

        if data['elements'].GetNumberOfCells() > 0:
            self.element_picker.Update()
            self.element_picker.Modified()

        if data['rbes'].GetNumberOfCells() > 0:
            self.rbe_picker.Update()
            self.rbe_picker.Modified()

    def node_pick(self, pos):

        data_set = self.node_picker.GetDataSet()

        if self.model_picker.get_renderer() is None or data_set is None or \
                        data_set.GetNumberOfCells() == 0:
            return False

        self.node_picker.Pick(pos[0], pos[1], 0, self.model_picker.get_renderer())

        _id = self.node_picker.GetPointId()

        if _id >= 0:

            global_id = data_set.GetCellData().GetGlobalIds().GetTuple(_id)[0]

            if self._last_selection == 'nodes %s' % str(global_id):
                return True

            self._last_selection = 'nodes %s' % str(global_id)

            self.selection = {'nodes': [global_id],
                              'elements': [],
                              'mpcs': [],
                              'loads': [],
                              'disps': []}

            self.model_picker.hover_data.Reset()
            self.model_picker.hover_data.ShallowCopy(self.node_picker.GetProjectedPoint())
            self.model_picker.hover_data.Modified()
            self.model_picker.render()

            return True
        else:
            return False


    def element_pick(self, pos):

        data_set = self.element_picker.GetDataSet()

        if self.model_picker.get_renderer() is None or data_set is None or \
                        data_set.GetNumberOfCells() == 0:
            return False

        self.element_picker.Pick(pos[0], pos[1], 0, self.model_picker.get_renderer())

        _id = self.element_picker.GetClosestCellId()

        if _id >= 0:

            global_id = self.element_picker.GetDataSet().GetCellData().GetGlobalIds().GetTuple(_id)[0]

            if self._last_selection == 'elements %s' % str(global_id):
                return True

            self._last_selection = 'elements %s' % str(global_id)

            self.selection = {'nodes': [],
                              'elements': [global_id],
                              'mpcs': [],
                              'loads': [],
                              'disps': []}

            self.model_picker.hover_data.Reset()
            self.model_picker.hover_data.DeepCopy(self.element_picker.GetClosestCellEdges())
            self.model_picker.hover_data.Modified()
            self.model_picker.render()

            return True
        else:
            return False

    def mouse_move(self, obj, event, interactor, action):

        should_pick = True

        if self._left_button_down or self._ctrl_left_button_down or self._middle_button_down or self._right_button_down:
            self.reset_hover_and_selected_data()
            should_pick = False

        action()

        if not should_pick:
            return

        pos = interactor.GetEventPosition()

        if self.model_picker.active_selections.nodes and self.node_pick(pos):
            pass
        elif self.model_picker.active_selections.elements and self.element_pick(pos):
            pass
        #elif self.poly_plane_picker.active_selections.rbes and self.pick(self.rbe_picker, pos):
        #    self.poly_plane_picker.render()
        else:
            self.reset_hover_data()

    def reset_hover_data(self, do_not_render=False):
        self._last_selection = None
        self.model_picker.hover_data.Reset()
        self.model_picker.hover_data.Modified()

        if not do_not_render:
            self.model_picker.render()

    def reset_hover_and_selected_data(self):
        self.reset_hover_data(True)
        self.model_picker.reset_selected_data()

    def try_pick(self):
        if self._down_pos == self._up_pos:
            self.something_picked()
        else:
            self.model_picker.update_selection_data()

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
            self.model_picker.update_selection_data()

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
            self.model_picker.update_selection_data()

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
            self.model_picker.update_selection_data()

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
            self.model_picker.update_selection_data()

    def mouse_wheel_forward(self, obj, event, interactor, action):
        self.reset_hover_and_selected_data()
        action()
        self.model_picker.update_selection_data()

    def mouse_wheel_backward(self, obj, event, interactor, action):
        self.reset_hover_and_selected_data()
        action()
        self.model_picker.update_selection_data()

    def set_picking(self, active_selections):

        self.node_picker.set_picking(VTK_VERTEX, active_selections.nodes)

        self.element_picker.set_picking(VTK_VERTEX, active_selections.points)
        self.element_picker.set_picking(VTK_LINE, active_selections.bars)
        self.element_picker.set_picking(VTK_TRI, active_selections.tris)
        self.element_picker.set_picking(VTK_QUAD, active_selections.quads)

        self.rbe_picker.set_picking(VTK_POLY_LINE, active_selections.rbes)

    def something_picked(self):
        self.reset_selection()

        if self._last_selection is not None:
            tmp = self._last_selection.split(' ')
            self.selection[tmp[0]] = int(round(float(tmp[1]), 0))

        self.model_picker.selection_list.update_selection(self.selection)