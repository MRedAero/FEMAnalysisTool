# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\CODE\10_PROJECT\FEMAnalysisTool\fem_post\view\dialogs\package_manager_ui.ui'
#
# Created: Sat Mar 28 08:52:09 2015
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

class Ui_Dialog_Plugins(object):
    def setupUi(self, Dialog_Plugins):
        Dialog_Plugins.setObjectName(_fromUtf8("Dialog_Plugins"))
        Dialog_Plugins.resize(569, 533)
        self.gridLayout = QtGui.QGridLayout(Dialog_Plugins)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line_3 = QtGui.QFrame(Dialog_Plugins)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 7, 0, 1, 1)
        self.lbl_plugins = QtGui.QLabel(Dialog_Plugins)
        self.lbl_plugins.setObjectName(_fromUtf8("lbl_plugins"))
        self.gridLayout.addWidget(self.lbl_plugins, 5, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_Plugins)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_setplugindir = QtGui.QPushButton(Dialog_Plugins)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_setplugindir.sizePolicy().hasHeightForWidth())
        self.btn_setplugindir.setSizePolicy(sizePolicy)
        self.btn_setplugindir.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_setplugindir.setObjectName(_fromUtf8("btn_setplugindir"))
        self.gridLayout_2.addWidget(self.btn_setplugindir, 0, 0, 1, 1)
        self.tedt_plugindir = TxtDrop(Dialog_Plugins)
        self.tedt_plugindir.setMaximumSize(QtCore.QSize(16777215, 50))
        self.tedt_plugindir.setObjectName(_fromUtf8("tedt_plugindir"))
        self.gridLayout_2.addWidget(self.tedt_plugindir, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        self.splitter = QtGui.QSplitter(Dialog_Plugins)
        self.splitter.setLineWidth(1)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(3)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tbl_plugins = QtGui.QTableWidget(self.splitter)
        self.tbl_plugins.setObjectName(_fromUtf8("tbl_plugins"))
        self.tbl_plugins.setColumnCount(0)
        self.tbl_plugins.setRowCount(0)
        self.tbrow_plugininfo = QtGui.QTextBrowser(self.splitter)
        self.tbrow_plugininfo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tbrow_plugininfo.setFrameShadow(QtGui.QFrame.Sunken)
        self.tbrow_plugininfo.setObjectName(_fromUtf8("tbrow_plugininfo"))
        self.gridLayout.addWidget(self.splitter, 6, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog_Plugins)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.btn_checkplugins = QtGui.QPushButton(Dialog_Plugins)
        self.btn_checkplugins.setMinimumSize(QtCore.QSize(200, 30))
        self.btn_checkplugins.setObjectName(_fromUtf8("btn_checkplugins"))
        self.gridLayout.addWidget(self.btn_checkplugins, 4, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog_Plugins)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 3, 0, 1, 1)
        self.line_2 = QtGui.QFrame(Dialog_Plugins)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog_Plugins)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_Plugins.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_Plugins.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Plugins)

    def retranslateUi(self, Dialog_Plugins):
        Dialog_Plugins.setWindowTitle(_translate("Dialog_Plugins", "Manage Plugins", None))
        self.lbl_plugins.setText(_translate("Dialog_Plugins", "Available Plugins:", None))
        self.btn_setplugindir.setText(_translate("Dialog_Plugins", "Specify Plugin Dir", None))
        self.label.setText(_translate("Dialog_Plugins", "Use the button to specify the plugins folder location from a dialog or drag and drop the plugins folder below.", None))
        self.btn_checkplugins.setText(_translate("Dialog_Plugins", "Check For Plugins", None))

from TxtDropWidget import TxtDrop

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog_Plugins = QtGui.QDialog()
    ui = Ui_Dialog_Plugins()
    ui.setupUi(Dialog_Plugins)
    Dialog_Plugins.show()
    sys.exit(app.exec_())

