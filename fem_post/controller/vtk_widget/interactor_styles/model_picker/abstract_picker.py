__author__ = 'Michael Redmond'


class AbstractPicker(object):
    def __init__(self, model_picker):
        super(AbstractPicker, self).__init__()

        self.model_picker = model_picker
        """:type : ModelPicker"""

    def left_button_down(self, obj, event, interactor):
        pass

    def left_button_double_click(self, obj, event, interactor):
        pass

    def ctrl_left_button_down(self, obj, event, interactor):
        pass

    def ctrl_left_button_up(self, obj, event, interactor):
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