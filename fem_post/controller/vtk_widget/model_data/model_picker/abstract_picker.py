__author__ = 'Michael Redmond'


class AbstractPicker(object):
    def __init__(self, model_picker):
        super(AbstractPicker, self).__init__()

        self.model_picker = model_picker
        """:type : ModelPicker"""

    def connect_signals(self):
        interactor_style = self.model_picker.interactor_style

        interactor_style.signals.left_button_down.connect(self.left_button_down)
        interactor_style.signals.left_button_double_click.connect(self.left_button_double_click)
        interactor_style.signals.ctrl_left_button_down.connect(self.ctrl_left_button_down)
        interactor_style.signals.ctrl_left_button_up.connect(self.ctrl_left_button_up)
        interactor_style.signals.left_button_up.connect(self.left_button_up)
        interactor_style.signals.middle_button_down.connect(self.middle_button_down)
        interactor_style.signals.middle_button_up.connect(self.middle_button_up)
        interactor_style.signals.right_button_down.connect(self.right_button_down)
        interactor_style.signals.right_button_up.connect(self.right_button_up)
        interactor_style.signals.mouse_wheel_forward.connect(self.mouse_wheel_forward)
        interactor_style.signals.mouse_wheel_backward.connect(self.mouse_wheel_backward)
        interactor_style.signals.mouse_move.connect(self.mouse_move)

    def disconnect_signals(self):
        interactor_style = self.model_picker.interactor_style

        interactor_style.signals.left_button_down.disconnect(self.left_button_down)
        interactor_style.signals.left_button_double_click.disconnect(self.left_button_double_click)
        interactor_style.signals.ctrl_left_button_down.disconnect(self.ctrl_left_button_down)
        interactor_style.signals.ctrl_left_button_up.disconnect(self.ctrl_left_button_up)
        interactor_style.signals.left_button_up.disconnect(self.left_button_up)
        interactor_style.signals.middle_button_down.disconnect(self.middle_button_down)
        interactor_style.signals.middle_button_up.disconnect(self.middle_button_up)
        interactor_style.signals.right_button_down.disconnect(self.right_button_down)
        interactor_style.signals.right_button_up.disconnect(self.right_button_up)
        interactor_style.signals.mouse_wheel_forward.disconnect(self.mouse_wheel_forward)
        interactor_style.signals.mouse_wheel_backward.disconnect(self.mouse_wheel_backward)
        interactor_style.signals.mouse_move.disconnect(self.mouse_move)

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