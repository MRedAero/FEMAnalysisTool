__author__ = 'Michael Redmond'

from PyQt4 import QtCore

from view import VTKSelectionsTestView

class VTKSelectionsTestAdaptor(object):
    def __init__(self, main_adaptor):
        super(VTKSelectionsTestAdaptor, self).__init__()

        self._main_adaptor = main_adaptor
        """:type: fem_post.application.adaptor.FemAnalysisToolAdaptor"""

        self._view = VTKSelectionsTestView()
        self._main_adaptor.add_dock_widget(QtCore.Qt.RightDockWidgetArea, self._view)

        self._view.ui.btn_show_hide.clicked.connect(self._show_hide)
        self._view.ui.btn_switch_view.clicked.connect(self._switch_view)

    def _show_hide(self):
        self._main_adaptor.show_hide()

    def _switch_view(self):
        self._main_adaptor.switch_view()


