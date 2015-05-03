__author__ = 'Michael Redmond'

from base_app.application.core.plugins import BaseAppPluginController

from vtk_selections_test import VTKSelectionsTestController


class FemAnalysisToolPluginController(BaseAppPluginController):
    def __init__(self, program_controller):
        super(FemAnalysisToolPluginController, self).__init__(program_controller)

        self._program_controller = self._program_controller
        """:type: fem_post.application.core.program_controller.FemAnalysisToolProgramController"""

        self._vtk_selections_test = VTKSelectionsTestController(self._program_controller)