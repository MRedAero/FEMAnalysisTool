__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub
from base_app.simple_pubsub import SimplePubSub

from base_app.utilities import BaseObject


class VTKBaseWidget(BaseObject):

    _active_vtk_widget = None
    """:type: VTKBaseWidget"""
    _actions = None
    _picking = None

    @classmethod
    def set_active_vtk(cls, vtk_widget):
        """

        :type vtk_widget: VTKBaseWidget
        """
        cls._active_vtk_widget = vtk_widget

    @classmethod
    def publish(cls, message, *args, **kwargs):
        cls._active_vtk_widget.get_pub().publish(message, *args, **kwargs)

    @classmethod
    def subscribe(cls, func, message):
        cls._active_vtk_widget.get_pub().subscribe(func, message)

    @classmethod
    def get_active_vtk_widget(cls):
        return cls._active_vtk_widget

    def __new__(cls, *args, **kwargs):
        instance = BaseObject.__new__(cls, *args, **kwargs)

        if cls._active_vtk_widget is None:
            cls._active_vtk_widget = instance

        if cls._actions is None:
            cls._actions = {'left_down': 'rotate_begin',
                            'ctrl_left_down': None,
                            'middle_down': 'pan_begin',
                            'right_down': 'zoom_begin',
                            'left_up': 'rotate_end',
                            'ctrl_left_up': None,
                            'middle_up': 'pan_end',
                            'right_up': 'zoom_end'}

        if cls._picking is None:
            cls._picking = {'left_down': False,
                            'ctrl_left_down': True,
                            'middle_down': False,
                            'right_down': False,
                            'left_up': False,
                            'ctrl_left_up': True,
                            'middle_up': False,
                            'right_up': False}

        return instance

    @classmethod
    def reset_picking(cls):
        cls._picking = {'left_down': False,
                        'ctrl_left_down': False,
                        'middle_down': False,
                        'right_down': False,
                        'left_up': False,
                        'ctrl_left_up': False,
                        'middle_up': False,
                        'right_up': False}

    @classmethod
    def set_button_action(cls, button, action):
        """

        :param button:
        :param action:
        :type button: str
        :type action: str
        :return:
        """

        button = button.upper()
        action = action.upper()

        if button == 'LEFT':
            down = 'left_down'
            up = 'left_up'
        elif button == 'RIGHT':
            down = 'right_down'
            up = 'right_up'
        elif button == 'MIDDLE':
            down = 'middle_down'
            up = 'middle_up'
        elif button == 'CTRL_LEFT':
            down = 'ctrl_left_down'
            up = 'ctrl_left_up'
        else:
            return

        picking = False

        if action == 'ROTATE':
            begin = 'rotate_begin'
            end = 'rotate_end'
        elif action == 'PAN':
            begin = 'pan_begin'
            end = 'pan_end'
        elif action == 'ZOOM':
            begin = 'zoom_begin'
            end = 'zoom_end'
        elif action == 'SELECT':
            begin = None
            end = None
            picking = True
        else:
            return

        cls._actions[down] = begin
        cls._actions[up] = end

        if picking:
            cls.reset_picking()
            cls._picking[down] = picking
            cls._picking[up] = picking

        for instance in cls._instances:
            instance.get_interactor_style().set_button_actions(cls._actions, cls._picking)

    def __init__(self, main_window):
        super(VTKBaseWidget, self).__init__()

        self._main_window = main_window

        self._interactor_style = None

        self._vtk_pub = SimplePubSub()
        """:type: SimplePubSub"""

    def get_interactor_style(self):
        return self._interactor_style

    def get_main_window(self):
        return self._main_window

    def get_pub(self):
        return self._vtk_pub
