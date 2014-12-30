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
        self._right_button_down = False
        self._middle_button_down = False

        self._down_pos = None
        self._up_pos = None

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

        if self.model_picker.get_renderer() is None:
            return False

        self.node_picker.Pick(pos[0], pos[1], 0, self.model_picker.get_renderer())

        _id = self.node_picker.GetPointId()

        if _id >= 0:

            if self._last_selection == 'Node %s' % str(_id):
                return True

            self._last_selection = 'Node %s' % str(_id)

            self.model_picker.hover_data.Reset()
            self.model_picker.hover_data.ShallowCopy(self.node_picker.GetProjectedPoint())
            self.model_picker.hover_data.Modified()
            self.model_picker.render()

            return True
        else:
            return False


    def element_pick(self, pos):

        if self.model_picker.get_renderer() is None:
            return False

        self.element_picker.Pick(pos[0], pos[1], 0, self.model_picker.get_renderer())

        _id = self.element_picker.GetClosestCellId()

        if _id >= 0:

            if self._last_selection == 'Element %s' % str(_id):
                return True

            self._last_selection = 'Element %s' % str(_id)

            self.model_picker.hover_data.Reset()
            self.model_picker.hover_data.DeepCopy(self.element_picker.GetClosestCellEdges())
            self.model_picker.hover_data.Modified()
            self.model_picker.render()

            return True
        else:
            return False

    def mouse_move(self, obj, event, interactor):

        if self._left_button_down or self._middle_button_down or self._right_button_down:
            self.no_selection()
            return

        pos = interactor.GetEventPosition()

        if self.model_picker.active_selections.nodes and self.node_pick(pos):
            pass
        elif self.model_picker.active_selections.elements and self.element_pick(pos):
            pass
        #elif self.poly_plane_picker.active_selections.rbes and self.pick(self.rbe_picker, pos):
        #    self.poly_plane_picker.render()
        else:
            self.no_selection()

    def no_selection(self):
        self._last_selection = None
        self.model_picker.hover_data.Reset()
        self.model_picker.hover_data.Modified()
        self.model_picker.render()

    def left_button_down(self, obj, event, interactor):
        self._left_button_down = True

        self._down_pos = interactor.GetEventPosition()

    def left_button_double_click(self, obj, event, interactor):
        pass

    def left_button_up(self, obj, event, interactor):
        self._left_button_down = False

        self._up_pos = interactor.GetEventPosition()

        if self._down_pos == self._up_pos:
            self.model_picker.selected_data.Reset()
            self.model_picker.selected_data.DeepCopy(self.model_picker.hover_data)
            self.model_picker.selected_data.Modified()
            self.model_picker.render()

    def middle_button_down(self, obj, event, interactor):
        self._middle_button_down = True

    def middle_button_up(self, obj, event, interactor):
        self._middle_button_down = False

    def right_button_down(self, obj, event, interactor):
        self._right_button_down = True

    def right_button_up(self, obj, event, interactor):
        self._right_button_down = False

    def mouse_wheel_forward(self, obj, event, interactor):
        self.no_selection()

    def mouse_wheel_backward(self, obj, event, interactor):
        self.no_selection()

    def set_picking(self, active_selections):

        self.node_picker.set_picking(VTK_VERTEX, active_selections.nodes)

        self.element_picker.set_picking(VTK_VERTEX, active_selections.points)
        self.element_picker.set_picking(VTK_LINE, active_selections.bars)
        self.element_picker.set_picking(VTK_TRI, active_selections.tris)
        self.element_picker.set_picking(VTK_QUAD, active_selections.quads)

        self.rbe_picker.set_picking(VTK_POLY_LINE, active_selections.rbes)