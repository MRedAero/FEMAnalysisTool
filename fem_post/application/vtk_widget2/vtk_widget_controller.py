__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub

from vtk_widget import VTKWidget


class VTKWidgetController(object):
    def __init__(self):
        self._vtk_widgets = []
        """:type: list [VTKWidget]"""

        self._active_vtk = None
        """:type: VTKWidget"""

        self._current_index = -1
        """:type: int"""

    def new_vtk(self, window):
        new_vtk = VTKWidget(window)

        self._vtk_widgets.append(new_vtk)

        self._active_vtk = new_vtk

        self._current_index = len(self._vtk_widgets) - 1

        new_vtk.initialize()

    def close_vtk(self, index):
        try:
            del self._vtk_widgets[index]
        except IndexError:
            pass

        self._active_vtk.unload()

        try:
            self._active_vtk = self._vtk_widgets[self._current_index]
        except IndexError:
            self._current_index -= 1
            if self._current_index >= 0:
                self._active_vtk = self._vtk_widgets[self._current_index]
            else:
                self._active_vtk = None

    def set_active_vtk(self, index):
        if index >= 0:
            self._active_vtk = self._vtk_widgets[index]

    def get_active_vtk(self):
        return self._active_vtk

    def switch_view(self):
        self._active_vtk.toggle_visible()

    def show_hide(self):
        self._active_vtk.toggle_selected()

    def __getattr__(self, attr):
        return getattr(self._active_vtk, attr)