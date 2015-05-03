__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.simple_pubsub import pub
from base_app.utilities.misc import new_name

from base_app.application.application import BaseAppProgramController

from plugins import FemAnalysisToolPluginController

from document import FemAnalysisToolDocumentController
from view import FemAnalysisToolViewController
from utilities import file_utilities


class FemAnalysisToolProgramController(BaseAppProgramController):
    def __init__(self, app):
        super(FemAnalysisToolProgramController, self).__init__(app)

        self._view_controller = self._view_controller
        """:type: FemAnalysisToolViewController"""

        self._document_controller = self._document_controller
        """:type: FemAnalysisToolDocumentController"""

    def create_document_controller(self, view_controller):
        return FemAnalysisToolDocumentController(view_controller)

    def create_view_controller(self, app):
        return FemAnalysisToolViewController(app)

    def create_plugin_controller(self):
        return FemAnalysisToolPluginController(self)

    def show_hide(self):
        pub.publish("vtk.show_hide")

    def switch_view(self):
        pub.publish("vtk.switch_view")

    def open_file(self, filename):
        h5_reader = file_utilities.open_file(filename)

        if not h5_reader:
            return

        vtk_widget = self._document_controller.get_active_vtk()

        if vtk_widget is None:
            self.new_file()
            vtk_widget = self._document_controller.get_active_vtk()

        self._app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            vtk_widget.set_file(h5_reader)
        finally:
            self._app.restoreOverrideCursor()