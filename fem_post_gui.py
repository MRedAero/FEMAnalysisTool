__author__ = 'Michael Redmond'

import sys
from PyQt4 import QtGui, QtCore

QtCore.Signal = QtCore.pyqtSignal

from fem_post.view import Ui_MainWindow
from fem_post.controller import MainWindow

import vtk.qt


vtk.qt.PyQtImpl = 'PyQt4'



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