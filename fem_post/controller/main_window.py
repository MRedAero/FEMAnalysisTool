
#!/usr/bin/env python

import sys

from PySide import QtGui

from .vtk import VTKController
from fem_reader.nastran.bdf.reader import BDFReader


class MainWindow(QtGui.QMainWindow):
 
    def __init__(self, ui):
        QtGui.QMainWindow.__init__(self)

        # Initiate the UI as defined by Qt Designer
        self.ui = ui
        self.ui.setupUi(self)

        self.vtk_controller = VTKController(self)

        self.ui.btn_bgcolor1.clicked.connect(self.on_color1)
        self.ui.btn_bgcolor2.clicked.connect(self.on_color2)
        self.ui.actionOpen.triggered.connect(self.on_open)

        self.bdf = None

        self.show()

    def on_color1(self):
        color = self.vtk_controller.bgcolor1
        initial_color = QtGui.QColor(255*color[0], 255*color[1], 255*color[2])
        color = QtGui.QColorDialog().getColor(initial_color, self)

        if not color.isValid():
            return

        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        color1 = (red, green, blue)
        self.vtk_controller.set_background_color(color1=color1)

    def on_color2(self):
        color = self.vtk_controller.bgcolor2
        initial_color = QtGui.QColor(255*color[0], 255*color[1], 255*color[2])
        color = QtGui.QColorDialog().getColor(initial_color, self)

        if not color.isValid():
            return

        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        color2 = (red, green, blue)
        self.vtk_controller.set_background_color(color2=color2)

    def on_open(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', None, "BDF Files (*.bdf);;DAT Files (*.dat)")

        if filename[0] == '':
            return

        self.bdf = BDFReader().read_bdf(filename[0])


if __name__ == "__main__":
 
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())