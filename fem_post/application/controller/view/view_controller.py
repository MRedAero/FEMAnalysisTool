__author__ = 'Michael Redmond'

from PyQt4 import QtCore, QtGui

from base_app.utilities.misc import new_name
from base_app.application.controller.view import BaseAppViewController

from fem_post.application.vtk_widget import VTKWidget
from fem_post.application.core.view import FemAnalysisToolViewCore


class FemAnalysisToolViewController(BaseAppViewController):
    def __init__(self, adaptor, app):

        super(FemAnalysisToolViewController, self).__init__(adaptor, app)

        self._adaptor = self._adaptor
        """:type: fem_post.application.adaptor.FemAnalysisToolAdaptor"""

        self._view = self._view
        """:type: FemAnalysisToolViewCore"""

        self._vtk_widgets = []
        """:type: list [VTKWidget]"""

        self._active_vtk = None
        """:type: VTKWidget"""

    @property
    def create_view_object(self):
        return FemAnalysisToolViewCore

    def new_document(self):

        """This is where new documents will originate from.
        Either the user will click on the new document action in the File menu,
        or the user will directly call this method when using the api."""

        model_names = self._adaptor.get_model_names()

        _new_name = new_name(model_names)

        self._is_active = True
        if not self._adaptor.new_model(_new_name):
            return
        self._is_active = False

        new_tab = QtGui.QWidget()
        new_tab.setObjectName(_new_name)
        new_tab.grid_layout = QtGui.QGridLayout(new_tab)

        new_vtk = VTKWidget(new_tab)

        new_tab.vtk_widget = new_vtk

        self._active_vtk = new_vtk

        new_vtk.initialize()

        self._vtk_widgets.append(new_vtk)

        self._view.add_tab(new_tab, _new_name)

    def close_document(self):

        if len(self._vtk_widgets) == 0:
            # nothing to close
            self._active_vtk = None
            return

        index = self._vtk_widgets.index(self._active_vtk)

        tab_to_close = self._active_vtk.get_parent()

        self._view.remove_tab(index)

        tab_to_close.setParent(None)

        self._is_active = True
        self._adaptor.close_model(index)
        self._is_active = False

    def _update_current_tab(self, index):
        super(FemAnalysisToolViewController, self)._update_current_tab(index)

        self._active_vtk = self._vtk_widgets[index]

    def _file_open(self):

        # noinspection PyCallByClass
        filename = QtGui.QFileDialog.getOpenFileName(self._view, 'Open File', "",
                                                     "BDF Files (*.bdf);;DAT Files (*.dat);;Database Files (*.h5)")

        if isinstance(filename, list):
            filename = filename[0]

        if filename == '':
            return

        filename = str(filename)

        if self._active_vtk is None:
            self.new_document()

        self._app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            self._is_active = True
            success = self._adaptor.open_file(filename)
            self._is_active = False

            if success:
                self._active_vtk.set_file(filename)
        finally:
            self._app.restoreOverrideCursor()

    def _file_save(self):
        print 'file save'

    def _file_save_as(self):
        print 'file save as'

    def _file_settings_plugins(self):
        print 'file settings plugins'

    def _file_exit(self):
        print 'file exit'

    def set_file(self, file):
        self._active_vtk.set_file(file)

    def show_hide(self):
        self._active_vtk.toggle_selected()

    def switch_view(self):
        self._active_vtk.toggle_visible()

    def get_central_widget(self):
        return self._view.central_widget

    def add_dock_widget(self, dock_area, dock_widget):
        self._view.addDockWidget(dock_area, dock_widget)
