# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\CODE\10_PROJECT\FEMAnalysisTool\fem_post\view\docks\dockui_message.ui'
#
# Created: Sun Mar 22 15:22:53 2015
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

class Ui_Dock_Message(object):
    def setupUi(self, Dock_Message):
        Dock_Message.setObjectName(_fromUtf8("Dock_Message"))
        Dock_Message.resize(652, 180)
        Dock_Message.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.txt_msg = QtGui.QPlainTextEdit(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_msg.sizePolicy().hasHeightForWidth())
        self.txt_msg.setSizePolicy(sizePolicy)
        self.txt_msg.setMinimumSize(QtCore.QSize(0, 0))
        self.txt_msg.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_msg.setObjectName(_fromUtf8("txt_msg"))
        self.gridLayout.addWidget(self.txt_msg, 0, 0, 1, 1)
        Dock_Message.setWidget(self.dockWidgetContents)

        self.retranslateUi(Dock_Message)
        QtCore.QMetaObject.connectSlotsByName(Dock_Message)

    def retranslateUi(self, Dock_Message):
        Dock_Message.setWindowTitle(_translate("Dock_Message", "Messages", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dock_Message = QtGui.QDockWidget()
    ui = Ui_Dock_Message()
    ui.setupUi(Dock_Message)
    Dock_Message.show()
    sys.exit(app.exec_())

