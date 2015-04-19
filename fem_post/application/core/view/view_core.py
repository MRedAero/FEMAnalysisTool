__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.application.core.view import BaseAppViewCore
from base_app.utilities.menus import MenuController


class FemAnalysisToolViewCore(BaseAppViewCore):
    def __init__(self):
        super(FemAnalysisToolViewCore, self).__init__()

        self.setObjectName("FemAnalysisToolViewCore")

        self.setWindowTitle("FEM Analysis Tool")


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    main_window = FemAnalysisToolViewCore()

    main_window.show()

    app.exec_()
