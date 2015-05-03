__author__ = 'Michael Redmond'

from PyQt4 import QtCore, QtGui

from base_app.simple_pubsub import pub
from base_app.application.core.view import BaseAppViewController

from fem_post.application.core.view import FemAnalysisToolViewCore


class FemAnalysisToolViewController(BaseAppViewController):
    def __init__(self, app):
        super(FemAnalysisToolViewController, self).__init__(app)

        self._view = self._view
        """:type: FemAnalysisToolViewCore"""

    def create_view_object(self):
        return FemAnalysisToolViewCore()

    def _file_open(self):
        # noinspection PyCallByClass
        filename = QtGui.QFileDialog.getOpenFileName(self._view, 'Open File', "",
                                                     "BDF Files (*.bdf);;DAT Files (*.dat);;HDF5 Files (*.h5)")

        if isinstance(filename, list):
            filename = filename[0]

        if filename == '':
            return

        filename = str(filename)

        self._app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            pub.publish('program.open_file', filename=filename)
        finally:
            self._app.restoreOverrideCursor()

    def get_central_widget(self):
        return self._view.central_widget

    def add_dock_widget(self, dock_area, dock_widget):
        self._view.addDockWidget(dock_area, dock_widget)
