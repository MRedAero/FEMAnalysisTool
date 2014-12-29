__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore


class InteractorSignals(QtCore.QObject):

    """Helper class that adds QT signals to DefaultInteractorStyle"""

    mouse_move = QtCore.Signal(object, object, object)
    left_button_down = QtCore.Signal(object, object, object)
    left_button_up = QtCore.Signal(object, object, object)
    middle_button_down = QtCore.Signal(object, object, object)
    middle_button_up = QtCore.Signal(object, object, object)
    right_button_down = QtCore.Signal(object, object, object)
    right_button_up = QtCore.Signal(object, object, object)
    mouse_wheel_forward = QtCore.Signal(object, object, object)
    mouse_wheel_backward = QtCore.Signal(object, object, object)
    left_button_double_click = QtCore.Signal(object, object, object)

    def __init__(self):
        super(InteractorSignals, self).__init__()


# noinspection PyUnusedLocal
class DefaultInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, widget):

        self.AddObserver("MouseMoveEvent", self.on_mouse_move)
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_down)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_up)
        self.AddObserver("MiddleButtonPressEvent", self.on_middle_button_down)
        self.AddObserver("MiddleButtonReleaseEvent", self.on_middle_button_up)
        self.AddObserver("RightButtonPressEvent", self.on_right_button_down)
        self.AddObserver("RightButtonReleaseEvent", self.on_right_button_up)
        self.AddObserver("MouseWheelForwardEvent", self.on_mouse_wheel_forward)
        self.AddObserver("MouseWheelBackwardEvent", self.on_mouse_wheel_backward)

        self.signals = InteractorSignals()

    def on_left_button_down(self, obj, event):
        if self.GetInteractor().GetRepeatCount() == 1:
            self.on_left_button_double_click(obj, event)
            return

        self.OnLeftButtonDown()

        self.signals.left_button_down.emit(obj, event, self.GetInteractor())

    def on_left_button_double_click(self, obj, event):
        self.signals.left_button_double_click.emit(obj, event, self.GetInteractor())

    def on_left_button_up(self, obj, event):
        self.OnLeftButtonUp()

        self.signals.left_button_up.emit(obj, event, self.GetInteractor())

    def on_middle_button_down(self, obj, event):
        self.OnMiddleButtonDown()

        self.signals.middle_button_down.emit(obj, event, self.GetInteractor())

    def on_middle_button_up(self, obj, event):
        self.OnMiddleButtonUp()

        self.signals.middle_button_up.emit(obj, event, self.GetInteractor())

    def on_right_button_down(self, obj, event):
        self.OnRightButtonDown()

        self.signals.right_button_down.emit(obj, event, self.GetInteractor())

    def on_right_button_up(self, obj, event):
        self.OnRightButtonUp()

        self.signals.right_button_up.emit(obj, event, self.GetInteractor())

    def on_mouse_wheel_forward(self, obj, event):
        self.OnMouseWheelForward()

        self.signals.mouse_wheel_forward.emit(obj, event, self.GetInteractor())

    def on_mouse_wheel_backward(self, obj, event):
        self.OnMouseWheelBackward()

        self.signals.mouse_wheel_backward.emit(obj, event, self.GetInteractor())

    def on_mouse_move(self, obj, event):
        self.OnMouseMove()

        self.signals.mouse_move.emit(obj, event, self.GetInteractor())

    def set_default_renderer(self, renderer):
        self.SetDefaultRenderer(renderer)
