__author__ = 'Michael Redmond'

from .abstract_picker import AbstractPicker
from ...custom_pickers import *
from .active_selections import ActiveSelections
from ...vtk_globals import *


class NoPicker(AbstractPicker):
    def __init__(self, model_picker):
        super(NoPicker, self).__init__(model_picker)

        self._left_button_down = False
        self._ctrl_left_button_down = False
        self._right_button_down = False
        self._middle_button_down = False

        self._down_pos = None
        self._up_pos = None

    def mouse_move(self, obj, event, interactor, action):
        action()

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

    def mouse_wheel_forward(self, obj, event, interactor, action):
        action()

    def mouse_wheel_backward(self, obj, event, interactor, action):
        action()