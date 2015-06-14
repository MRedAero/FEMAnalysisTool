__author__ = 'Michael Redmond'

from fem_post.application.vtk_widget.vtk_globals import vtk_globals
from fem_post.application.vtk_widget.algorithms.abstract_split_data_filter import AbstractSplitDataFilter


class SplitDataFilter(AbstractSplitDataFilter):
    def __init__(self):
        AbstractSplitDataFilter.__init__(self)

        self.add_category('node', vtk_globals.CATEGORY_SELECTION['node'])
        self.add_category('vertex', vtk_globals.CATEGORY_SELECTION['vertex'])
        self.add_category('element', vtk_globals.CATEGORY_SELECTION['element'])
        self.add_category('mpc', vtk_globals.CATEGORY_SELECTION['mpc'])
        self.add_category('force', vtk_globals.CATEGORY_SELECTION['force'])
        self.add_category('disp', vtk_globals.CATEGORY_SELECTION['disp'])
        self.add_category('coord', vtk_globals.CATEGORY_SELECTION['coord'])

    def node_port(self):
        return self.get_output_port_by_name('node')

    def vertex_port(self):
        return self.get_output_port_by_name('vertex')

    def element_port(self):
        return self.get_output_port_by_name('element')

    def mpc_port(self):
        return self.get_output_port_by_name('mpc')

    def force_port(self):
        return self.get_output_port_by_name('force')

    def disp_port(self):
        return self.get_output_port_by_name('disp')

    def coord_port(self):
        return self.get_output_port_by_name('coord')

    def node_data(self):
        return self.get_output_data_by_name('node')

    def vertex_data(self):
        return self.get_output_data_by_name('vertex')

    def element_data(self):
        return self.get_output_data_by_name('element')

    def mpc_data(self):
        return self.get_output_data_by_name('mpc')

    def force_data(self):
        return self.get_output_data_by_name('force')

    def disp_data(self):
        return self.get_output_data_by_name('disp')

    def coord_data(self):
        return self.get_output_data_by_name('coord')