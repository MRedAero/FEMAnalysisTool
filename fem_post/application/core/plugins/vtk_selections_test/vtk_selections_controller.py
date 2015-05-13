__author__ = 'Michael Redmond'

from PyQt4 import QtCore

from base_app.simple_pubsub import pub

from fem_post.application.vtk_widget import VTKWidget

from view import VTKSelectionsTestView


class VTKSelectionsTestController(object):
    def __init__(self, program_controller):
        super(VTKSelectionsTestController, self).__init__()

        self._program_controller = program_controller
        """:type: fem_post.application.core.program_controller.FemAnalysisToolProgramController"""

        self._program_view_controller = self._program_controller.get_view_controller()

        self._view = VTKSelectionsTestView()
        self._program_view_controller.add_dock_widget(QtCore.Qt.RightDockWidgetArea, self._view)

        self._view.ui.btn_show_hide.clicked.connect(self._show_hide)
        self._view.ui.btn_switch_view.clicked.connect(self._switch_view)

        self._view.ui.cbx_left_click.setCurrentIndex(0)
        self._view.ui.cbx_middle_click.setCurrentIndex(1)
        self._view.ui.cbx_right_click.setCurrentIndex(2)
        self._view.ui.cbx_ctrl_left_click.setCurrentIndex(3)

        self._view.ui.cbx_left_click.currentIndexChanged[str].connect(self._cbx_left_click)
        self._view.ui.cbx_middle_click.currentIndexChanged[str].connect(self._cbx_middle_click)
        self._view.ui.cbx_right_click.currentIndexChanged[str].connect(self._cbx_right_click)
        self._view.ui.cbx_ctrl_left_click.currentIndexChanged[str].connect(self._cbx_ctrl_left_click)

        self._is_active = True

        pub.subscribe(self._set_selection_box, "vtk.set_selection_box")

        self._view.clicked.connect(self._clicked)

    def set_active(self):
        self._is_active = True

    def set_inactive(self):
        self._is_active = False

    def _clicked(self):
        self.set_inactive()
        pub.publish("plugins.set_active_plugin", self)

    def _show_hide(self):
        self._program_controller.show_hide()

    def _switch_view(self):
        self._program_controller.switch_view()

    def _cbx_left_click(self, value):
        VTKWidget.set_button_action('left', str(value))

    def _cbx_middle_click(self, value):
        VTKWidget.set_button_action('middle', str(value))

    def _cbx_right_click(self, value):
        VTKWidget.set_button_action('right', str(value))

    def _cbx_ctrl_left_click(self, value):
        VTKWidget.set_button_action('ctrl_left', str(value))

    def _set_selection_box(self, selection):
        if not self._is_active:
            return

        self._view.ui.lnedt_selection.setText(selection)
        self._view.ui.lnedt_selection.setCursorPosition(0)