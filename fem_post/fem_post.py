__author__ = 'Michael Redmond'

# modifies sys.path for external_tools
import external_tools

import sys
from PySide import QtGui

from base_app.application import BaseApplication

from view import Ui_MainWindow
from controller import MainWindow


def main():

    app = BaseApplication(sys.argv)

    model = None
    view = Ui_MainWindow()
    controller = MainWindow(app, model, view)

    app.build(controller)

    app.start()