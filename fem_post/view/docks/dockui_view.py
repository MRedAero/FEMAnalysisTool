# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\CODE\10_PROJECT\FEMAnalysisTool\fem_post\view\docks\dockui_view.ui'
#
# Created: Sun Mar 22 06:53:04 2015
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

class Ui_Dock_View(object):
    def setupUi(self, Dock_View):
        Dock_View.setObjectName(_fromUtf8("Dock_View"))
        Dock_View.resize(190, 454)
        Dock_View.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_switch = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_switch.setObjectName(_fromUtf8("btn_switch"))
        self.gridLayout.addWidget(self.btn_switch, 5, 0, 1, 1)
        self.btn_elementcolor = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_elementcolor.setObjectName(_fromUtf8("btn_elementcolor"))
        self.gridLayout.addWidget(self.btn_elementcolor, 7, 0, 1, 1)
        self.btn_nofillededge = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_nofillededge.setObjectName(_fromUtf8("btn_nofillededge"))
        self.gridLayout.addWidget(self.btn_nofillededge, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 150, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 1)
        self.btn_togglewire = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_togglewire.setObjectName(_fromUtf8("btn_togglewire"))
        self.gridLayout.addWidget(self.btn_togglewire, 8, 0, 1, 1)
        self.btn_bgcolor2 = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_bgcolor2.setObjectName(_fromUtf8("btn_bgcolor2"))
        self.gridLayout.addWidget(self.btn_bgcolor2, 1, 0, 1, 1)
        self.btn_perspectivetoggle = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_perspectivetoggle.setObjectName(_fromUtf8("btn_perspectivetoggle"))
        self.gridLayout.addWidget(self.btn_perspectivetoggle, 6, 0, 1, 1)
        self.btn_saveimg = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_saveimg.setObjectName(_fromUtf8("btn_saveimg"))
        self.gridLayout.addWidget(self.btn_saveimg, 9, 0, 1, 1)
        self.btn_edgecolor = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_edgecolor.setObjectName(_fromUtf8("btn_edgecolor"))
        self.gridLayout.addWidget(self.btn_edgecolor, 3, 0, 1, 1)
        self.btn_bgcolor1 = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_bgcolor1.sizePolicy().hasHeightForWidth())
        self.btn_bgcolor1.setSizePolicy(sizePolicy)
        self.btn_bgcolor1.setObjectName(_fromUtf8("btn_bgcolor1"))
        self.gridLayout.addWidget(self.btn_bgcolor1, 0, 0, 1, 1)
        Dock_View.setWidget(self.dockWidgetContents)

        self.retranslateUi(Dock_View)
        QtCore.QMetaObject.connectSlotsByName(Dock_View)

    def retranslateUi(self, Dock_View):
        Dock_View.setToolTip(_translate("Dock_View", "View Dock", None))
        Dock_View.setStatusTip(_translate("Dock_View", "View Utilities Dock", None))
        Dock_View.setWindowTitle(_translate("Dock_View", "View", None))
        self.btn_switch.setToolTip(_translate("Dock_View", "Switch Background for Printing", None))
        self.btn_switch.setText(_translate("Dock_View", "Switch", None))
        self.btn_elementcolor.setText(_translate("Dock_View", "Element Color", None))
        self.btn_nofillededge.setText(_translate("Dock_View", "No Filled Edge", None))
        self.btn_togglewire.setText(_translate("Dock_View", "Toggle Wire", None))
        self.btn_bgcolor2.setText(_translate("Dock_View", "BG 2 Color", None))
        self.btn_perspectivetoggle.setText(_translate("Dock_View", "Toggle Pers.", None))
        self.btn_saveimg.setText(_translate("Dock_View", "Save IMG", None))
        self.btn_edgecolor.setText(_translate("Dock_View", "Edge Color", None))
        self.btn_bgcolor1.setText(_translate("Dock_View", "BG 1 Color", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dock_View = QtGui.QDockWidget()
    ui = Ui_Dock_View()
    ui.setupUi(Dock_View)
    Dock_View.show()
    sys.exit(app.exec_())

