# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PGM\01_DEV\VTK\MVC\view.ui'
#
# Created: Wed Oct 29 07:46:45 2014
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
#from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(673, 606)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_perspectivetoggle = QtGui.QPushButton(self.centralwidget)
        self.btn_perspectivetoggle.setObjectName(_fromUtf8("btn_perspectivetoggle"))
        self.gridLayout.addWidget(self.btn_perspectivetoggle, 6, 0, 1, 1)
        self.btn_bgcolor1 = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_bgcolor1.sizePolicy().hasHeightForWidth())
        self.btn_bgcolor1.setSizePolicy(sizePolicy)
        self.btn_bgcolor1.setObjectName(_fromUtf8("btn_bgcolor1"))
        self.gridLayout.addWidget(self.btn_bgcolor1, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.vl = QtGui.QVBoxLayout()
        self.vl.setObjectName(_fromUtf8("vl"))
        self.gridLayout_2.addLayout(self.vl, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 1, 10, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 1)
        self.btn_saveimg = QtGui.QPushButton(self.centralwidget)
        self.btn_saveimg.setObjectName(_fromUtf8("btn_saveimg"))
        self.gridLayout.addWidget(self.btn_saveimg, 8, 0, 1, 1)
        self.btn_nofillededge = QtGui.QPushButton(self.centralwidget)
        self.btn_nofillededge.setObjectName(_fromUtf8("btn_nofillededge"))
        self.gridLayout.addWidget(self.btn_nofillededge, 4, 0, 1, 1)
        self.btn_switch = QtGui.QPushButton(self.centralwidget)
        self.btn_switch.setObjectName(_fromUtf8("btn_switch"))
        self.gridLayout.addWidget(self.btn_switch, 5, 0, 1, 1)
        self.btn_bgcolor2 = QtGui.QPushButton(self.centralwidget)
        self.btn_bgcolor2.setObjectName(_fromUtf8("btn_bgcolor2"))
        self.gridLayout.addWidget(self.btn_bgcolor2, 1, 0, 1, 1)
        self.btn_edgecolor = QtGui.QPushButton(self.centralwidget)
        self.btn_edgecolor.setObjectName(_fromUtf8("btn_edgecolor"))
        self.gridLayout.addWidget(self.btn_edgecolor, 2, 0, 1, 1)
        self.btn_elementcolor = QtGui.QPushButton(self.centralwidget)
        self.btn_elementcolor.setObjectName(_fromUtf8("btn_elementcolor"))
        self.gridLayout.addWidget(self.btn_elementcolor, 3, 0, 1, 1)
        self.btn_togglewire = QtGui.QPushButton(self.centralwidget)
        self.btn_togglewire.setObjectName(_fromUtf8("btn_togglewire"))
        self.gridLayout.addWidget(self.btn_togglewire, 7, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 673, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.txt_msg = QtGui.QPlainTextEdit(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_msg.sizePolicy().hasHeightForWidth())
        self.txt_msg.setSizePolicy(sizePolicy)
        self.txt_msg.setMinimumSize(QtCore.QSize(0, 120))
        self.txt_msg.setMaximumSize(QtCore.QSize(16777215, 120))
        self.txt_msg.setObjectName(_fromUtf8("txt_msg"))
        self.gridLayout_3.addWidget(self.txt_msg, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_perspectivetoggle.setText(_translate("MainWindow", "Toggle Pers.", None))
        self.btn_bgcolor1.setText(_translate("MainWindow", "BG 1 Color", None))
        self.btn_saveimg.setText(_translate("MainWindow", "Save IMG", None))
        self.btn_nofillededge.setText(_translate("MainWindow", "No Filled Edge", None))
        self.btn_switch.setToolTip(_translate("MainWindow", "Switch Background for Printing", None))
        self.btn_switch.setText(_translate("MainWindow", "Switch", None))
        self.btn_bgcolor2.setText(_translate("MainWindow", "BG 2 Color", None))
        self.btn_edgecolor.setText(_translate("MainWindow", "Edge Color", None))
        self.btn_elementcolor.setText(_translate("MainWindow", "Element Color", None))
        self.btn_togglewire.setText(_translate("MainWindow", "Toggle Wire", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

