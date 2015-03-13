__author__ = 'Michael Redmond'

import vtk

from ..custom_pickers import vtkNodeCellPicker2


class NodeCellFilter(vtk.vtkProgrammableFilter):
    def __init__(self):
        self.SetExecuteMethod(self.execute)

        self.node_picker = vtkNodeCellPicker2()
        self.node_picker.SetTolerance(0.005)

    def add_pick_list(self, actor):
        self.node_picker.add_pick_list(actor)

    def pick(self, x, y, z, renderer):
        self.node_picker.Pick(x, y, z, renderer)

    def get_cell_id(self):
        return self.node_picker.GetCellId()

    def execute(self):
        self.node_picker.update_node_filter_data()
        self.GetOutput().ShallowCopy(self.node_picker.GetClosestCell())