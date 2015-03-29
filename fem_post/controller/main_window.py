__author__ = 'Michael Redmond'

import os
from PyQt4 import QtGui, QtCore

from .vtk_widget2 import VTKWidget
from fem_reader.nastran.bdf.reader import BDFReader

from dock_control import Dock_Picking
from dock_control import Dock_View
from dock_control import Dock_Message
from dock_control import Dock_Preferences

from dock_control import Dialog_Plugins

class MainWindow(QtGui.QMainWindow):
 
    def __init__(self, app, ui):
        QtGui.QMainWindow.__init__(self)

        self.app = app
        """:type : QApplication"""
        self.ui = ui
        self.ui.setupUi(self)
        self.ui.menubar.setNativeMenuBar(False)


        # Setup Dock Ui(s)
        self.picking = Dock_Picking()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.picking)

        self.view = Dock_View()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.view)

        self.message = Dock_Message()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.message)
        self.message.show()
        self.msg_minsize = [50,50]
        self.msg_defaultsize = [50,50]


        self.preferences = Dock_Preferences()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.preferences)
        self.preferences.setFloating(True)
        self.preferences.hide()
        self.connect(self.ui.action_Preferences, QtCore.SIGNAL('triggered()'), self.on_preferences)
        self.connect(self.preferences, QtCore.SIGNAL('topLevelChanged(bool)'), self.on_dockpreflvlchange)
        self.prefdocksize = [500,500]
        self.prefdockgutter = 50
        self.connect(self.preferences.ui.dial_iconsize, QtCore.SIGNAL('valueChanged(int)'), self.on_icondial)
        self.connect(self.preferences.ui.lnedt_iconsize, QtCore.SIGNAL('returnPressed()'), self.on_manualicon)

        self.default_iconsize = 24

        self.tabifyDockWidget(self.picking, self.view)
        self.view.raise_()


        # Resize the Window
        self.minsize = [150,100]
        self.defaultsize = [1000,800] # not golden ratio
        self.setMinimumSize(self.minsize[0], self.minsize[1])
        self.resize(self.defaultsize[0], self.defaultsize[1])


        # Plugins Dialog
        self.manager = Dialog_Plugins()
        self.connect(self.ui.action_Plugin_Manager, QtCore.SIGNAL('triggered()'), self.on_plugin_manager)
        # Connect the custom signal from the txt_edit
        self.connect(self.manager.ui.tedt_plugindir, QtCore.SIGNAL('dropped'), self.on_drop_plugin_dir)
        self.plugin_dir = os.path.abspath('../plugins')


        # Initialize style if available
        # todo: possibly class the stylesheet instead of reading a file
        self.usrstylefile = r'stylesheet.dat'
        self.usrstyle()

        # Setup Connections
        self.ui.action_Open.triggered.connect(self.on_open)
        self.ui.action_elementvis.triggered.connect(self.on_elementvis)
        self.ui.action_nodevis.triggered.connect(self.on_nodevis)
        self.ui.action_elementvis.setChecked(True)
        self.ui.action_nodevis.setChecked(True)
        self.ui.action_Quit.triggered.connect(self.on_close)

        self.view.ui.btn_bgcolor1.clicked.connect(self.on_color1)
        self.view.ui.btn_bgcolor2.clicked.connect(self.on_color2)
        self.view.ui.btn_perspectivetoggle.clicked.connect(self.on_toggle_perspective)

        self.picking.ui.btn_toggle_view.clicked.connect(self.toggle_visible)
        self.picking.ui.btn_toggle_hidden.clicked.connect(self.toggle_selected)

        self.picking.ui.btn_single_pick.clicked.connect(self.single_pick_button)
        self.picking.ui.btn_box_pick.clicked.connect(self.box_pick_button)
        self.picking.ui.btn_poly_pick.clicked.connect(self.poly_pick_button)

        self.picking.ui.btn_any.clicked.connect(self.any_button)
        self.picking.ui.btn_nodes.clicked.connect(self.nodes_button)
        self.picking.ui.btn_elements.clicked.connect(self.elements_button)
        self.picking.ui.btn_points.clicked.connect(self.points_button)
        self.picking.ui.btn_bars.clicked.connect(self.bars_button)
        self.picking.ui.btn_tris.clicked.connect(self.tris_button)
        self.picking.ui.btn_quads.clicked.connect(self.quads_button)

        self.picking.ui.btn_replace_selection.clicked.connect(self.replace_selection_button)
        self.picking.ui.btn_append_selection.clicked.connect(self.append_selection_button)
        self.picking.ui.btn_remove_selection.clicked.connect(self.remove_selection_button)

        self.picking.ui.cbx_left_click.setCurrentIndex(0)
        self.picking.ui.cbx_middle_click.setCurrentIndex(1)
        self.picking.ui.cbx_right_click.setCurrentIndex(2)
        self.picking.ui.cbx_ctrl_left_click.setCurrentIndex(3)



        self.dock_resize()





        self.bdf = None

        # http://www.paraview.org/Wiki/VTK/Examples/Python/Widgets/EmbedPyQt
        # http://www.vtk.org/pipermail/vtk-developers/2013-July/014005.html
        # see above why self.show() is not implemented here
        # it is implemented inside VTKWidget.view
        #self.show()

        self.vtk_widget = VTKWidget(self)


    def on_drop_plugin_dir(self,drpfile):
        self.manager.ui.tedt_plugindir.clear()
        self.manager.ui.tedt_plugindir.setText(drpfile)

    def on_check_plugins(self):
        """ Checks the specified location for plugs and populates the available plugins table

            Note:  still in development.. need to clean up


        :returns
           empty if user cancels dialog
                note:  need to store initial checked states

           list of checked items in order to run plugin activation on if user selects ok
        """


        # clear the table
        self.manager.ui.tbl_plugins.clear()


        # todo:  where to instantiate the manager?
        from manager import PluginManager
        pm = PluginManager()

        pm.add_plugin_folder(self.plugin_dir)
        pm.collect_plugins()

        plugins = pm.get_plugins()
        print plugins

        columns = 3
        categories = plugins.keys()

        # list comprehension to get plugin name list... need number of plugins for setting table ros
        plugin_names = [plugin for category in categories for plugin in plugins[category].keys()]
        print plugin_names

        num_plugins = len(plugin_names)

        print('Found %s Total Plugins' % num_plugins)

        rows = num_plugins
        self.manager.ui.tbl_plugins.setRowCount(rows)
        self.manager.ui.tbl_plugins.setColumnCount(columns)
        self.manager.ui.tbl_plugins.verticalHeader().setVisible(False)

        self.manager.ui.tbl_plugins.setHorizontalHeaderLabels(['Activate','Plugin Name','Category'])


        #todo: print remove
        print('Number of Plugins found: %s' % str(rows))


        #todo: ... maybe use a tree
        #
        # plugins is ordereddict where [0] is category
        #       [1] is another ordereddict

        # list plugins in table
        row=0
        for category in categories:
            category_plugins = plugins[category].keys()
            for plugin in category_plugins:

                item0 = QtGui.QTableWidgetItem('')
                item1 = QtGui.QTableWidgetItem('%s' % plugin)
                item2 = QtGui.QTableWidgetItem('%s' % category)

                #if row % 2:
                #if row > 0:
                item0.setFlags(QtCore.Qt.ItemIsUserCheckable |
                              QtCore.Qt.ItemIsEnabled)
                item0.setCheckState(QtCore.Qt.Unchecked)

                self.manager.ui.tbl_plugins.setItem(row, 0, item0)
                self.manager.ui.tbl_plugins.setItem(row, 1, item1)
                self.manager.ui.tbl_plugins.setItem(row, 2, item2)

                print('added item')
                row += 1

        self._list = []
        self.manager.ui.tbl_plugins.itemClicked.connect(self.handleItemClicked)


    def handleItemClicked(self, item):
        # todo:  still buggy
        if item.checkState() == QtCore.Qt.Checked:
            print('"%s" Checked' % item.text())
            self._list.append(item.row())
            print(self._list)
        elif item.checkState() == QtCore.Qt.Unchecked:
            print('"%s" Un-Checked' % item.text())
            self._list.remove(item.row())
            print(self._list)
        else:
            print('"%s" Clicked' % item.text())
            print(self._list)


    def print_check(self):
        print('something happened')


    def on_get_plugin_dir(self):
        user_dir = str(QtGui.QFileDialog.getExistingDirectory(self, "Specify Plugin Directory.", self.plugin_dir))
        if user_dir:
            self.plugin_dir = user_dir

        self.on_set_plugin_dir(self.plugin_dir)

        self.manager.activateWindow()


    def on_set_plugin_dir(self,dir):
        self.manager.ui.tedt_plugindir.setText(dir)

    def on_plugin_manager(self):

        # Set the plugin directory.... default if not changed
        self.on_set_plugin_dir(self.plugin_dir)

        #Connect
        self.manager.ui.btn_setplugindir.pressed.connect(self.on_get_plugin_dir)
        self.manager.ui.btn_checkplugins.pressed.connect(self.on_check_plugins)

        # check for plugins when manager opens (default the directory)
        self.on_check_plugins()

        self.manager.ui.splitter.setSizes([500,300])


        # Set the Window Title
        self.manager.setWindowTitle("Plugin Manager")
        #icon = QtGui.QIcon(self.iconpath)
        #manager.setWindowIcon(icon)
        ret = self.manager.exec_()
        print('User Selected: %s' % ret)

        if ret == 0:
            return # Cancel Flag is 0

        self.on_check_plugins()



    def on_icondial(self):

        val = self.preferences.ui.dial_iconsize.value()
        self.set_iconsize(val)
        self.preferences.ui.lnedt_iconsize.setText(str(val))

    def on_manualicon(self):

        try:
            val = float(self.preferences.ui.lnedt_iconsize.text())
        except ValueError:
            self.preferences.ui.lnedt_iconsize.setText(str(self.default_iconsize))
            self.set_iconsize(self.default_iconsize)
            return

        if val >= 16 and val <= 56:
            self.set_iconsize(val)
        else:
            # todo: redundant with above... rework
            self.preferences.ui.lnedt_iconsize.setText(str(self.default_iconsize))
            self.set_iconsize(self.default_iconsize)

    def set_iconsize(self,size):
        print("sizing")
        self.ui.tbar_grp.setIconSize(QtCore.QSize(size,size))
        self.ui.tbar_1.setIconSize(QtCore.QSize(size,size))
        self.ui.tbar_showhide.setIconSize(QtCore.QSize(size,size))


    def dock_resize(self):
        # todo:  why is this not resizing the msg dock?
        self.message.setMinimumSize(self.msg_minsize[0], self.msg_minsize[1])
        self.message.resize(self.msg_defaultsize[0], self.msg_defaultsize[1])

    def on_close(self):
        self.close()

    def on_dockpreflvlchange(self):
        """ pref dock level change.... handle accordingly
        """
        # If its not floating... its docked.. and we don't want it docked
        if not self.preferences.isFloating():
            self.preferences.setEnabled(False)
            self.preferences.hide()

    def on_preferences(self):
        self.preferences.setEnabled(True)
        self.preferences.show()
        self.preferences.raise_()
        self.preferences.setFloating(True)
        self.preferences.setMinimumSize(QtCore.QSize(self.prefdocksize[0],self.prefdocksize[1]))
        self.preferences.resize(QtCore.QSize(self.prefdocksize[0],self.prefdocksize[1]))
        #self.preferences.move(self.x()+self.size().width()+self.dock_gutter,self.y())
        self.preferences.move(self.x()+self.prefdockgutter,self.y()+self.prefdockgutter)


    def usrstyle(self):

        print(self.usrstylefile)
        if os.path.isfile(self.usrstylefile):
            print "usrstyle file found, reading"
            with open(self.usrstylefile, 'r') as fsty:
                style = fsty.read()
            fsty.close()

            self.setStyleSheet(style)

            #TODO: Style for manager dialog
            self.manager.setStyleSheet(style)

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

        # For PySide, dir as None ok... For PyQt, dir must be QString()
        #filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', None, "BDF Files (*.bdf);;DAT Files (*.dat)")
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open File','',"BDF Files (*.bdf);;DAT Files (*.dat)")

        if filename[0] == '':
            return

        self.bdf = BDFReader()

        # noinspection PyUnresolvedReferences
        self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        # For PyQt - send reader "filename" .. for PySide - send reader "filename[0]"
        #self.bdf.read_bdf(filename[0])
        self.bdf.read_bdf(filename)

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

    def on_elementvis(self):
        # todo: add vtk_widget function to toggle element visibility
        if self.ui.action_elementvis.isChecked():
            self.vtk_widget.toggle_elements('ON')
        else:
            self.vtk_widget.toggle_elements('OFF')

    def on_nodevis(self):
        # todo: add vtk_widget function to toggle node visibility
        if self.ui.action_nodevis.isChecked():
            self.vtk_widget.toggle_nodes('ON')
        else:
            self.vtk_widget.toggle_nodes('OFF')

    # todo: add vtk_widget function to adjust model rotation (pivot) point
    # todo: add vtk_widget function to change element color
    # todo: add vtk_widget function to change node color / size
    # todo: add vtk_widget function to change element filled edge line color / thickness
    # todo: add vtk_widget function to change show / hide element filled edges
    # todo: add vtk_widget function to support wireframe view
    # todo: add vtk_widget function to fit view all in window ... this should be the default open behavior
    # todo: add vtk_widget functions for zoom in / zoom out (for buttons in toolbar)



