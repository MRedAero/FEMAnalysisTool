__author__ = 'Michael Redmond'

from PySide import QtGui, QtCore

from .vtk_widget2 import VTKWidget
from fem_reader.nastran.bdf.reader import BDFReader


class MainWindow(QtGui.QMainWindow):
 
    def __init__(self, app, ui):
        QtGui.QMainWindow.__init__(self)

        self.app = app
        """:type : QApplication"""
        self.ui = ui
        self.ui.setupUi(self)
        self.ui.menubar.setNativeMenuBar(False)

        self.ui.btn_bgcolor1.clicked.connect(self.on_color1)
        self.ui.btn_bgcolor2.clicked.connect(self.on_color2)
        self.ui.actionOpen.triggered.connect(self.on_open)
        self.ui.btn_perspectivetoggle.clicked.connect(self.on_toggle_perspective)

        self.ui.toggle_view_button.clicked.connect(self.toggle_visible)
        self.ui.toggle_hidden_button.clicked.connect(self.toggle_selected)

        self.ui.single_pick_button.clicked.connect(self.single_pick_button)
        self.ui.box_pick_button.clicked.connect(self.box_pick_button)
        self.ui.poly_pick_button.clicked.connect(self.poly_pick_button)

        self.ui.any_button.clicked.connect(self.any_button)
        self.ui.nodes_button.clicked.connect(self.nodes_button)
        self.ui.elements_button.clicked.connect(self.elements_button)
        self.ui.points_button.clicked.connect(self.points_button)
        self.ui.bars_button.clicked.connect(self.bars_button)
        self.ui.tris_button.clicked.connect(self.tris_button)
        self.ui.quads_button.clicked.connect(self.quads_button)

        self.ui.replace_selection_button.clicked.connect(self.replace_selection_button)
        self.ui.append_selection_button.clicked.connect(self.append_selection_button)
        self.ui.remove_selection_button.clicked.connect(self.remove_selection_button)

        self.ui.left_click_combo.setCurrentIndex(0)
        self.ui.middle_click_combo.setCurrentIndex(1)
        self.ui.right_click_combo.setCurrentIndex(2)
        self.ui.ctrl_left_click_combo.setCurrentIndex(3)

        self.bdf = None

        # http://www.paraview.org/Wiki/VTK/Examples/Python/Widgets/EmbedPyQt
        # http://www.vtk.org/pipermail/vtk-developers/2013-July/014005.html
        # see above why self.show() is not implemented here
        # it is implemented inside VTKWidget.view
        #self.show()

        self.vtk_widget = VTKWidget(self)

    def on_color1(self):
        color = self.vtk_widget.bg_color_1
        initial_color = QtGui.QColor(255*color[0], 255*color[1], 255*color[2])
        color = QtGui.QColorDialog().getColor(initial_color, self)

        if not color.isValid():
            return

        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        color1 = (red, green, blue)
        self.vtk_widget.set_background_color(color1=color1)

    def on_color2(self):
        color = self.vtk_widget.bg_color_2
        initial_color = QtGui.QColor(255*color[0], 255*color[1], 255*color[2])
        color = QtGui.QColorDialog().getColor(initial_color, self)

        if not color.isValid():
            return

        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        color2 = (red, green, blue)
        self.vtk_widget.set_background_color(color2=color2)

    def on_open(self):
        # noinspection PyCallByClass
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', None, "BDF Files (*.bdf);;DAT Files (*.dat)")

        if filename[0] == '':
            return

        self.bdf = BDFReader()

        # noinspection PyUnresolvedReferences
        self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.bdf.read_bdf(filename[0])
        self.vtk_widget.set_bdf_data(self.bdf)
        # noinspection PyUnresolvedReferences
        self.app.restoreOverrideCursor()

        self.bdf = None

    def on_toggle_perspective(self):
        self.vtk_widget.toggle_perspective()

    def toggle_selected(self):
        self.vtk_widget.toggle_selected()

    def toggle_visible(self):
        self.vtk_widget.toggle_visible()

    def single_pick_button(self):
        self.vtk_widget.single_pick_button()

    def box_pick_button(self):
        self.vtk_widget.box_pick_button()

    def poly_pick_button(self):
        self.vtk_widget.poly_pick_button()

    def any_button(self):
        self.vtk_widget.toggle_picking(0)

    def nodes_button(self):
        self.vtk_widget.toggle_picking(1)

    def elements_button(self):
        self.vtk_widget.toggle_picking(2)

    def points_button(self):
        self.vtk_widget.toggle_picking(2, 1)

    def bars_button(self):
        self.vtk_widget.toggle_picking(2, 2)

    def tris_button(self):
        self.vtk_widget.toggle_picking(2, 3)

    def quads_button(self):
        self.vtk_widget.toggle_picking(2, 4)

    def replace_selection_button(self):
        self.vtk_widget.replace_selection_button()

    def append_selection_button(self):
        self.vtk_widget.append_selection_button()

    def remove_selection_button(self):
        self.vtk_widget.remove_selection_button()

