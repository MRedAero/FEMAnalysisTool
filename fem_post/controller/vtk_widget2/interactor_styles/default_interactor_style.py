__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore

from .model_picker import ModelPicker


# can be deleted
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

        self.model_picker = ModelPicker(self.vtk_widget, self)

        self.active_picker = self.model_picker.single_picker

        self.AddObserver("MouseMoveEvent", self.on_mouse_move)
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_down)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_up)
        self.AddObserver("MiddleButtonPressEvent", self.on_middle_button_down)
        self.AddObserver("MiddleButtonReleaseEvent", self.on_middle_button_up)
        self.AddObserver("RightButtonPressEvent", self.on_right_button_down)
        self.AddObserver("RightButtonReleaseEvent", self.on_right_button_up)
        self.AddObserver("MouseWheelForwardEvent", self.on_mouse_wheel_forward)
        self.AddObserver("MouseWheelBackwardEvent", self.on_mouse_wheel_backward)

        #self.signals = InteractorSignals()

        self.rotate_begin = self.OnLeftButtonDown
        self.pan_begin = self.OnMiddleButtonDown
        self.zoom_begin = self.OnRightButtonDown
        self.rotate_end = self.OnLeftButtonUp
        self.pan_end = self.OnMiddleButtonUp
        self.zoom_end = self.OnRightButtonUp

        self.single_picking_active = False
        self.box_picking_active = False
        self.poly_picking_active = False

        self.mouse_button_pressed = False

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

    def set_selection_type(self, selection_type):
        self.model_picker.set_selection_type(selection_type)

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

    def on_left_button_down(self, obj, event):

        self.mouse_button_pressed = True

        ctrl_key = self.GetInteractor().GetControlKey()
        shift_key = self.GetInteractor().GetShiftKey()

        # give box picking priority over poly picking
        if ctrl_key:
            shift_key = False

        #if ctrl_key and shift_key:
        #    self.ctrl_shift_pressed = True
        #    self.on_ctrl_shift_button_click(obj, event)
        #    return

        if ctrl_key:
            self.box_picking_active = True
            self.model_picker.box_picker.begin_picking(self.GetInteractor())
            return
        else:
            self.box_picking_active = False

        if self.poly_picking_active:
            if self.model_picker.poly_picker.add_point(self.GetInteractor()):
                self.poly_picking_active = False
            return

        elif shift_key:
            self.poly_picking_active = True
            self.model_picker.poly_picker.begin_picking(self.GetInteractor())
            return

        if self.GetInteractor().GetRepeatCount():
            self.on_left_button_double_click(obj, event)
            return

        self.model_picker.single_picker.begin_picking(self.GetInteractor())
        self.single_picking_active = True

        self.actions['left_down']()

    def on_ctrl_left_button_click(self, obj, event):
        self.active_picker.ctrl_left_button_down(obj, event, self.GetInteractor(),
                                            self.actions['ctrl_left_down'], self.picking['ctrl_left_down'])

    def on_left_button_double_click(self, obj, event):
        pass
        #self.active_picker.left_button_double_click(obj, event, self.GetInteractor(), None, None)

    def on_left_button_up(self, obj, event):
        if self.box_picking_active:
            self.box_picking_active = False
            self.model_picker.box_picker.end_picking(self.GetInteractor())

        #elif self.poly_picking_active:
            #self.poly_picking_active = False
            #self.model_picker.poly_picker.end_picking(self.GetInteractor())

        elif self.single_picking_active:
            self.model_picker.single_picker.end_picking(self.GetInteractor())

        self.actions['left_up']()

        self.mouse_button_pressed = False

    def on_middle_button_down(self, obj, event):
        self.actions['middle_down']()

        self.mouse_button_pressed = False

    def on_middle_button_up(self, obj, event):
        self.actions['middle_up']()

        self.mouse_button_pressed = False

    def on_right_button_down(self, obj, event):
        self.actions['right_down']()

        self.mouse_button_pressed = True

    def on_right_button_up(self, obj, event):
        self.actions['right_up']()

        self.mouse_button_pressed = False

    def on_mouse_wheel_forward(self, obj, event):
        self.OnMouseWheelForward()

    def on_mouse_wheel_backward(self, obj, event):
        self.OnMouseWheelBackward()

    def on_mouse_move(self, obj, event):
        if self.box_picking_active:
            self.model_picker.box_picker.mouse_move(self.GetInteractor())
            return

        elif self.poly_picking_active:
            self.model_picker.poly_picker.mouse_move(self.GetInteractor())
            return

        elif not self.mouse_button_pressed:
            self.model_picker.single_picker.mouse_move(self.GetInteractor())

        self.OnMouseMove()

    def set_default_renderer(self, renderer):
        self.SetDefaultRenderer(renderer)
