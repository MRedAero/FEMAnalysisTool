__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore


class InteractorSignals(QtCore.QObject):

    """Helper class that adds QT signals to DefaultInteractorStyle"""

    mouse_move = QtCore.Signal(object, object, object, object)
    mouse_wheel_forward = QtCore.Signal(object, object, object, object)
    mouse_wheel_backward = QtCore.Signal(object, object, object, object)

    left_button_down = QtCore.Signal(object, object, object, object, object)
    left_button_up = QtCore.Signal(object, object, object, object, object)

    middle_button_down = QtCore.Signal(object, object, object, object, object)
    middle_button_up = QtCore.Signal(object, object, object, object, object)

    right_button_down = QtCore.Signal(object, object, object, object, object)
    right_button_up = QtCore.Signal(object, object, object, object, object)

    ctrl_left_button_down = QtCore.Signal(object, object, object, object, object)
    ctrl_left_button_up = QtCore.Signal(object, object, object, object, object)

    left_button_double_click = QtCore.Signal(object, object, object, object)

    def __init__(self):
        super(InteractorSignals, self).__init__()


# noinspection PyUnusedLocal
class DefaultInteractorStyle(vtk.vtkInteractorStyleRubberBandPick):

    def __init__(self, vtk_widget):

        self.vtk_widget = vtk_widget

        self.AddObserver("MouseMoveEvent", self.on_mouse_move)
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_down)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_up)
        self.AddObserver("MiddleButtonPressEvent", self.on_middle_button_down)
        self.AddObserver("MiddleButtonReleaseEvent", self.on_middle_button_up)
        self.AddObserver("RightButtonPressEvent", self.on_right_button_down)
        self.AddObserver("RightButtonReleaseEvent", self.on_right_button_up)
        self.AddObserver("MouseWheelForwardEvent", self.on_mouse_wheel_forward)
        self.AddObserver("MouseWheelBackwardEvent", self.on_mouse_wheel_backward)
        #self.AddObserver("CharEvent", self.on_char)

        self.signals = InteractorSignals()

        self.rotate_begin = self.OnLeftButtonDown
        self.pan_begin = self.OnMiddleButtonDown
        self.zoom_begin = self.OnRightButtonDown
        self.rotate_end = self.OnLeftButtonUp
        self.pan_end = self.OnMiddleButtonUp
        self.zoom_end = self.OnRightButtonUp

        self.ctrl_pressed = False

        self.actions = {'left_down': self.rotate_begin,
                        'ctrl_left_down': None,
                        'middle_down': self.pan_begin,
                        'right_down': self.zoom_begin,
                        'left_up': self.rotate_end,
                        'ctrl_left_up': None,
                        'middle_up': self.pan_end,
                        'right_up': self.zoom_end}

        self.picking = {'left_down': False,
                        'ctrl_left_down': True,
                        'middle_down': False,
                        'right_down': False,
                        'left_up': False,
                        'ctrl_left_up': True,
                        'middle_up': False,
                        'right_up': False}

    def reset_picking(self):
        self.picking = {'left_down': False,
                        'ctrl_left_down': False,
                        'middle_down': False,
                        'right_down': False,
                        'left_up': False,
                        'ctrl_left_up': False,
                        'middle_up': False,
                        'right_up': False}

    def set_left_button(self, action):
        self._set_button('left_down', 'left_up', action)

    def set_middle_button(self, action):
        self._set_button('middle_down', 'middle_up', action)

    def set_right_button(self, action):
        self._set_button('right_down', 'right_up', action)

    def set_ctrl_left_button(self, action):
        self._set_button('ctrl_left_down', 'ctrl_left_up', action)

    def _set_button(self, button_down, button_up, action):
        if action == 'Rotate':
            begin = self.rotate_begin
            end = self.rotate_end
        elif action == 'Pan':
            begin = self.pan_begin
            end = self.pan_end
        elif action == 'Zoom':
            begin = self.zoom_begin
            end = self.zoom_end
        elif action == 'Select':
            begin = None
            end = None
            self.reset_picking()
            self.picking[button_down] = True
            self.picking[button_up] = True

        self.actions[button_down] = begin
        self.actions[button_up] = end

    def on_char(self, obj, event):
        self.OnChar()
        print 'on char'

    def on_left_button_down(self, obj, event):

        if self.GetInteractor().GetControlKey():
            self.ctrl_pressed = True
            self.on_ctrl_left_button_click(obj, event)
            return

        self.ctrl_pressed = False

        if self.GetInteractor().GetRepeatCount():
            self.on_left_button_double_click(obj, event)
            return

        self.signals.left_button_down.emit(obj, event, self.GetInteractor(),
                                           self.actions['left_down'], self.picking['left_down'])

    def on_ctrl_left_button_click(self, obj, event):
        self.signals.ctrl_left_button_down.emit(obj, event, self.GetInteractor(),
                                                self.actions['ctrl_left_down'], self.picking['ctrl_left_down'])

    def on_left_button_double_click(self, obj, event):
        self.signals.left_button_double_click.emit(obj, event, self.GetInteractor(), None)

    def on_left_button_up(self, obj, event):
        if self.ctrl_pressed:
            self.ctrl_pressed = False
            self.signals.ctrl_left_button_up.emit(obj, event, self.GetInteractor(),
                                                  self.actions['ctrl_left_up'], self.picking['ctrl_left_up'])
            return

        self.signals.left_button_up.emit(obj, event, self.GetInteractor(),
                                         self.actions['left_up'], self.picking['left_up'])

    def on_middle_button_down(self, obj, event):
        self.signals.middle_button_down.emit(obj, event, self.GetInteractor(),
                                             self.actions['middle_down'], self.picking['middle_down'])

    def on_middle_button_up(self, obj, event):
        self.signals.middle_button_up.emit(obj, event, self.GetInteractor(),
                                           self.actions['middle_up'], self.picking['middle_up'])

    def on_right_button_down(self, obj, event):
        self.signals.right_button_down.emit(obj, event, self.GetInteractor(),
                                            self.actions['right_down'], self.picking['right_down'])

    def on_right_button_up(self, obj, event):
        self.signals.right_button_up.emit(obj, event, self.GetInteractor(),
                                          self.actions['right_up'], self.picking['right_up'])

    def on_mouse_wheel_forward(self, obj, event):
        self.signals.mouse_wheel_forward.emit(obj, event, self.GetInteractor(), self.OnMouseWheelForward)

    def on_mouse_wheel_backward(self, obj, event):
        self.signals.mouse_wheel_backward.emit(obj, event, self.GetInteractor(), self.OnMouseWheelBackward)

    def on_mouse_move(self, obj, event):
        self.signals.mouse_move.emit(obj, event, self.GetInteractor(), self.OnMouseMove)

    def set_default_renderer(self, renderer):
        self.SetDefaultRenderer(renderer)
