__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub
from base_app.application.core.plugins import BaseAppPluginController

from vtk_selections_test import VTKSelectionsTestController


class FemAnalysisToolPluginController(BaseAppPluginController):
    def __init__(self, program_controller):
        super(FemAnalysisToolPluginController, self).__init__(program_controller)

        self._program_controller = self._program_controller
        """:type: fem_post.application.core.program_controller.FemAnalysisToolProgramController"""

        self._vtk_selections_test = VTKSelectionsTestController(self._program_controller)
        self._core_plugins.append(self._vtk_selections_test)

        pub.subscribe(self._set_active_plugin, "plugins.set_active_plugin")

    def _set_active_plugin(self, active_plugin):
        print active_plugin
        for plugin in self._core_plugins:
            if plugin is active_plugin:
                plugin.set_active()
                return

        for plugin in self._external_plugins:
            if plugin is active_plugin:
                plugin.set_active()
                return