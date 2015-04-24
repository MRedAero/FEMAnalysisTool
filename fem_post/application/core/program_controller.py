__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

import gc

from base_app.simple_pubsub import pub
from base_app.application.application import BaseAppProgramController
from base_app.utilities.misc import new_name

from fem_post.application.vtk_widget import VTKWidgetController

from fem_post.application.core.plugins import PluginController

from model import FemAnalysisToolModelController
from view import FemAnalysisToolViewController
from utilities import file_utilities


class FemAnalysisToolProgramController(BaseAppProgramController):
    def __init__(self, app):

        self._vtk_controller = VTKWidgetController()

        super(FemAnalysisToolProgramController, self).__init__(app)

        self._model_controller = self._model_controller
        """:type: FemAnalysisToolModelController"""

        self._view_controller = self._view_controller
        """:type: FemAnalysisToolViewCore"""

        self._plugin_controller = PluginController(self)

    def create_model_controller_object(self):
        return FemAnalysisToolModelController()

    def create_view_controller_object(self, app):
        return FemAnalysisToolViewController(app)

    def get_view_controller(self):
        return self._view_controller

    def get_vtk_controller(self):
        return self._vtk_controller

    def get_model_controller(self):
        return self._model_controller

    def new_file(self):
        super(FemAnalysisToolProgramController, self).new_file()

        view = self._view_controller.get_active_view()
        self._vtk_controller.new_vtk(view)

    def set_active_document(self, index):
        super(FemAnalysisToolProgramController, self).set_active_document(index)

        self._vtk_controller.set_active_vtk(index)

    def open_file(self, filename):
        h5_reader = file_utilities.open_file(filename)

        if not h5_reader:
            return

        vtk_widget = self._vtk_controller.get_active_vtk()

        if vtk_widget is None:
            self.new_file()
            vtk_widget = self._vtk_controller.get_active_vtk()

        self._app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            vtk_widget.set_file(h5_reader)
        finally:
            self._app.restoreOverrideCursor()

    def close_file(self, index):
        self._view_controller.close_view(index)
        self._model_controller.close_model(index)
        self._vtk_controller.close_vtk(index)

        #if index:
        #    try:
        #        self.set_active_document(index)
        #    except Exception:
        #        self.set_active_document(index-1)

        #self._vtk_controller._vtk_widgets = []

        gc.collect()