__author__ = 'Michael Redmond'

from vtk_selections_test import VTKSelectionsTestController


class PluginController(object):
    def __init__(self, program_controller):
        super(PluginController, self).__init__()

        self._program_controller = program_controller
        """:type: fem_post.application.core.program_controller.FemAnalysisToolProgramController"""

        self._view_controller = self._program_controller.get_view_controller()

        self._vtk_controller = self._program_controller.get_vtk_controller()

        self._vtk_selections_test = VTKSelectionsTestController(self._program_controller)