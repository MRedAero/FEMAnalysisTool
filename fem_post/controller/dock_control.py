__author__ = 'Nick Wilson'

from PyQt4 import QtGui,QtCore

from view import Ui_Dock_Picking
from view import Ui_Dock_View
from view import Ui_Dock_Message
from view import Ui_Dock_Preferences

from view import Ui_Dialog_Plugins


class Dock_Picking(QtGui.QDockWidget):
    def __init__(self, parent=None):
        QtGui.QDockWidget.__init__(self, parent)
        self.ui = Ui_Dock_Picking()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        self.emit(QtCore.SIGNAL("closed"))


class Dock_View(QtGui.QDockWidget):
    def __init__(self, parent=None):
        QtGui.QDockWidget.__init__(self, parent)
        self.ui = Ui_Dock_View()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        self.emit(QtCore.SIGNAL("closed"))

class Dock_Message(QtGui.QDockWidget):
    def __init__(self, parent=None):
        QtGui.QDockWidget.__init__(self, parent)
        self.ui = Ui_Dock_Message()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        self.emit(QtCore.SIGNAL("closed"))


class Dock_Preferences(QtGui.QDockWidget):
    def __init__(self, parent=None):
        QtGui.QDockWidget.__init__(self, parent)
        self.ui = Ui_Dock_Preferences()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        self.emit(QtCore.SIGNAL("closed"))

class Dialog_Plugins(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDockWidget.__init__(self, parent)
        self.ui = Ui_Dialog_Plugins()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        self.emit(QtCore.SIGNAL("closed"))