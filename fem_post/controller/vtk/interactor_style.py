__author__ = 'Michael Redmond'

import vtk


class DefaultInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self):
        self.AddObserver("MouseMoveEvent", self.on_mouse_move)
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_down)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_up)
        self.AddObserver("MiddleButtonPressEvent", self.on_middle_button_down)
        self.AddObserver("MiddleButtonReleaseEvent", self.on_middle_button_up)
        self.AddObserver("RightButtonPressEvent", self.on_right_button_down)
        self.AddObserver("RightButtonReleaseEvent", self.on_right_button_up)
        self.AddObserver("MouseWheelForwardEvent", self.on_mouse_wheel_forward)
        self.AddObserver("MouseWheelBackwardEvent", self.on_mouse_wheel_backward)

    def on_mouse_move(self, obj, event):
        self.OnMouseMove()

    def on_left_button_down(self, obj, event):
        self.OnLeftButtonDown()

    def on_left_button_up(self, obj, event):
        self.OnLeftButtonUp()

    def on_middle_button_down(self, obj, event):
        self.OnMiddleButtonDown()

    def on_middle_button_up(self, obj, event):
        self.OnMiddleButtonUp()

    def on_right_button_down(self, obj, event):
        self.OnMiddleButtonUp()

    def on_right_button_up(self, obj, event):
        self.OnRightButtonUp()

    def on_mouse_wheel_forward(self, obj, event):
        self.OnMouseWheelForward()

    def on_mouse_wheel_backward(self, obj, event):
        self.OnMouseWheelBackward()