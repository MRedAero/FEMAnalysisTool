__author__ = 'Michael Redmond'

from PyQt4 import QtGui

from external_plugin_ui import Ui_DockWidget


class ExternalPluginView(QtGui.QDockWidget):
    def __init__(self):
        super(ExternalPluginView, self).__init__()

        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
