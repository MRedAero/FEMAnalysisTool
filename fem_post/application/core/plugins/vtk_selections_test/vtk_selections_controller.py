__author__ = 'Michael Redmond'

from PyQt4 import QtCore

from view import VTKSelectionsTestView

class VTKSelectionsTestController(object):
    def __init__(self, program_controller):
        super(VTKSelectionsTestController, self).__init__()

        self._program_controller = program_controller
        """:type: fem_post.application.core.program_controller.FemAnalysisToolProgramController"""

        self._program_view_controller = self._program_controller.get_view_controller()
        self._program_vtk_controller = self._program_controller.get_vtk_controller()

        self._view = VTKSelectionsTestView()
        self._program_view_controller.add_dock_widget(QtCore.Qt.RightDockWidgetArea, self._view)

        self._view.ui.btn_show_hide.clicked.connect(self._show_hide)
        self._view.ui.btn_switch_view.clicked.connect(self._switch_view)

    def _show_hide(self):
        self._program_vtk_controller.show_hide()

    def _switch_view(self):
        self._program_vtk_controller.switch_view()