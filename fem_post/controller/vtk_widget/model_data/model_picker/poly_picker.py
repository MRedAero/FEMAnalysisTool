__author__ = 'Michael Redmond'

from .abstract_picker import AbstractPicker


class PolyPicker(AbstractPicker):
    def __init__(self, model_picker):
        super(PolyPicker, self).__init__(model_picker)

        self.model_picker = model_picker

    def left_button_down(self, obj, event, interactor):
        pass

    def left_button_double_click(self, obj, event, interactor):
        pass

    def left_button_up(self, obj, event, interactor):
        pass

    def middle_button_down(self, obj, event, interactor):
        pass

    def middle_button_up(self, obj, event, interactor):
        pass

    def right_button_down(self, obj, event, interactor):
        pass

    def right_button_up(self, obj, event, interactor):
        pass

    def mouse_wheel_forward(self, obj, event, interactor):
        pass

    def mouse_wheel_backward(self, obj, event, interactor):
        pass

    def mouse_move(self, obj, event, interactor):
        pass