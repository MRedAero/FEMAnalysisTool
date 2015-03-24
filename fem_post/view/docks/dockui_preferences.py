# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\CODE\10_PROJECT\FEMAnalysisTool\fem_post\view\docks\dockui_preferences.ui'
#
# Created: Tue Mar 24 05:55:31 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dock_Preferences(object):
    def setupUi(self, Dock_Preferences):
        Dock_Preferences.setObjectName(_fromUtf8("Dock_Preferences"))
        Dock_Preferences.resize(248, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dock_Preferences.sizePolicy().hasHeightForWidth())
        Dock_Preferences.setSizePolicy(sizePolicy)
        Dock_Preferences.setFloating(True)
        Dock_Preferences.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        Dock_Preferences.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.line_2 = QtGui.QFrame(self.dockWidgetContents)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 2)
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 2)
        self.lbl_iconsize = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_iconsize.sizePolicy().hasHeightForWidth())
        self.lbl_iconsize.setSizePolicy(sizePolicy)
        self.lbl_iconsize.setObjectName(_fromUtf8("lbl_iconsize"))
        self.gridLayout.addWidget(self.lbl_iconsize, 1, 0, 1, 1)
        self.lnedt_iconsize = QtGui.QLineEdit(self.dockWidgetContents)
        self.lnedt_iconsize.setObjectName(_fromUtf8("lnedt_iconsize"))
        self.gridLayout.addWidget(self.lnedt_iconsize, 2, 0, 1, 1)
        self.dial_iconsize = QtGui.QDial(self.dockWidgetContents)
        self.dial_iconsize.setMinimum(16)
        self.dial_iconsize.setMaximum(56)
        self.dial_iconsize.setWrapping(True)
        self.dial_iconsize.setNotchTarget(8.0)
        self.dial_iconsize.setNotchesVisible(True)
        self.dial_iconsize.setObjectName(_fromUtf8("dial_iconsize"))
        self.gridLayout.addWidget(self.dial_iconsize, 1, 1, 2, 1)
        Dock_Preferences.setWidget(self.dockWidgetContents)

        self.retranslateUi(Dock_Preferences)
        QtCore.QMetaObject.connectSlotsByName(Dock_Preferences)

    def retranslateUi(self, Dock_Preferences):
        Dock_Preferences.setWindowTitle(_translate("Dock_Preferences", "Preferences", None))
        self.lbl_iconsize.setText(_translate("Dock_Preferences", "Icon Size (px)", None))
        self.lnedt_iconsize.setText(_translate("Dock_Preferences", "24", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dock_Preferences = QtGui.QDockWidget()
    ui = Ui_Dock_Preferences()
    ui.setupUi(Dock_Preferences)
    Dock_Preferences.show()
    sys.exit(app.exec_())

