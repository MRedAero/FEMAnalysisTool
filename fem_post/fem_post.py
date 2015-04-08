__author__ = 'Michael Redmond'

# modifies sys.path for external_tools
import external_tools

import sys
from PySide import QtGui

from view import Ui_MainWindow
from controller import MainWindow


def main():

    app = QtGui.QApplication(sys.argv)
    # model ... fem data and other user data?
    view = Ui_MainWindow()
    controller = MainWindow(app, view)
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()

    #import cProfile
    #filename = "fem_post_profile.stats"
    #cProfile.run('main()', filename)


    #from pycallgraph import PyCallGraph
    #from pycallgraph.output import GraphvizOutput
    #with PyCallGraph(output=GraphvizOutput()):
    #    main()