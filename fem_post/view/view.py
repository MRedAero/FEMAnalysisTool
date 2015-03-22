# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\CODE\10_PROJECT\FEMAnalysisTool\fem_post\view\view.ui'
#
# Created: Sun Mar 22 15:23:21 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(741, 652)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.frame = QtGui.QFrame(self.splitter)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.vl = QtGui.QVBoxLayout()
        self.vl.setObjectName(_fromUtf8("vl"))
        self.gridLayout_2.addLayout(self.vl, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 741, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Group = QtGui.QMenu(self.menubar)
        self.menu_Group.setObjectName(_fromUtf8("menu_Group"))
        self.menu_Tools = QtGui.QMenu(self.menubar)
        self.menu_Tools.setObjectName(_fromUtf8("menu_Tools"))
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName(_fromUtf8("menu_View"))
        self.menu_Toolbars = QtGui.QMenu(self.menu_View)
        self.menu_Toolbars.setObjectName(_fromUtf8("menu_Toolbars"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.tbar_grp = QtGui.QToolBar(MainWindow)
        self.tbar_grp.setObjectName(_fromUtf8("tbar_grp"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tbar_grp)
        self.tbar_1 = QtGui.QToolBar(MainWindow)
        self.tbar_1.setMovable(True)
        self.tbar_1.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.tbar_1.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.tbar_1.setFloatable(True)
        self.tbar_1.setObjectName(_fromUtf8("tbar_1"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tbar_1)
        self.action_A1 = QtGui.QAction(MainWindow)
        self.action_A1.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/qrc/074.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_A1.setIcon(icon)
        self.action_A1.setObjectName(_fromUtf8("action_A1"))
        self.action_A2 = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/qrc/002.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_A2.setIcon(icon1)
        self.action_A2.setObjectName(_fromUtf8("action_A2"))
        self.action_A3 = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/qrc/097.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_A3.setIcon(icon2)
        self.action_A3.setObjectName(_fromUtf8("action_A3"))
        self.action_GRP1 = QtGui.QAction(MainWindow)
        self.action_GRP1.setObjectName(_fromUtf8("action_GRP1"))
        self.action_GRP2 = QtGui.QAction(MainWindow)
        self.action_GRP2.setObjectName(_fromUtf8("action_GRP2"))
        self.action_GRP3 = QtGui.QAction(MainWindow)
        self.action_GRP3.setObjectName(_fromUtf8("action_GRP3"))
        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setObjectName(_fromUtf8("action_Open"))
        self.action_View = QtGui.QAction(MainWindow)
        self.action_View.setCheckable(True)
        self.action_View.setObjectName(_fromUtf8("action_View"))
        self.action_Picking = QtGui.QAction(MainWindow)
        self.action_Picking.setObjectName(_fromUtf8("action_Picking"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.action_Quit)
        self.menu_Toolbars.addAction(self.action_View)
        self.menu_Toolbars.addAction(self.action_Picking)
        self.menu_View.addAction(self.menu_Toolbars.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Group.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.tbar_grp.addAction(self.action_GRP1)
        self.tbar_grp.addAction(self.action_GRP2)
        self.tbar_grp.addAction(self.action_GRP3)
        self.tbar_1.addAction(self.action_A1)
        self.tbar_1.addAction(self.action_A2)
        self.tbar_1.addAction(self.action_A3)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menu_Group.setTitle(_translate("MainWindow", "&Group", None))
        self.menu_Tools.setTitle(_translate("MainWindow", "&Tools", None))
        self.menu_View.setTitle(_translate("MainWindow", "&View", None))
        self.menu_Toolbars.setTitle(_translate("MainWindow", "&Toolbars", None))
        self.tbar_grp.setWindowTitle(_translate("MainWindow", "Grouping Toolbar", None))
        self.tbar_grp.setToolTip(_translate("MainWindow", "Group Toolbar", None))
        self.tbar_grp.setStatusTip(_translate("MainWindow", "Group Tools", None))
        self.tbar_1.setWindowTitle(_translate("MainWindow", "toolBar_2", None))
        self.action_A1.setText(_translate("MainWindow", "&A1", None))
        self.action_A2.setText(_translate("MainWindow", "&A2", None))
        self.action_A3.setText(_translate("MainWindow", "&A3", None))
        self.action_GRP1.setText(_translate("MainWindow", "&GRP1", None))
        self.action_GRP2.setText(_translate("MainWindow", "GRP2", None))
        self.action_GRP3.setText(_translate("MainWindow", "GRP3", None))
        self.action_Open.setText(_translate("MainWindow", "&Open...", None))
        self.action_View.setText(_translate("MainWindow", "&View", None))
        self.action_Picking.setText(_translate("MainWindow", "&Picking", None))
        self.action_Quit.setText(_translate("MainWindow", "&Quit", None))

import viewqrc_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

