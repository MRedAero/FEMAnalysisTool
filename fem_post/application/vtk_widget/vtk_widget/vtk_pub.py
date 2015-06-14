__author__ = 'Michael Redmond'

from .vtk_base_widget import VTKBaseWidget

_show_hide = 'vtk.show_hide'
_switch_view = 'vtk.switch_view'
_fit_view = 'vtk.fit_view'
_render = 'vtk.render'


def set_active_vtk(vtk_widget):
    VTKBaseWidget.set_active_vtk(vtk_widget)


class _Publish(object):
    """
    Publishes messages to the to the active vtk widget.
    """
    @staticmethod
    def show_hide():
        VTKBaseWidget.publish(_show_hide)

    @staticmethod
    def switch_view():
        VTKBaseWidget.publish(_switch_view)

    @staticmethod
    def fit_view():
        VTKBaseWidget.publish(_fit_view)

    @staticmethod
    def render():
        VTKBaseWidget.publish(_render)


class _Subscribe(object):
    """
    Retrieves pub messages for vtk widget in order to subscribe to them.
    """
    @staticmethod
    def show_hide():
        return _show_hide

    @staticmethod
    def switch_view():
        return _switch_view

    @staticmethod
    def fit_view():
        return _fit_view

    @staticmethod
    def render():
        return _render


publish = _Publish()
subscribe = _Subscribe()