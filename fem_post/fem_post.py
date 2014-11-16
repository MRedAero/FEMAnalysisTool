__author__ = 'Michael Redmond'

import sys
from PySide import QtGui

from view import Ui_MainWindow
from controller import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    # model ... fem data and other user data?
    view = Ui_MainWindow()
    controller = MainWindow(view)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()