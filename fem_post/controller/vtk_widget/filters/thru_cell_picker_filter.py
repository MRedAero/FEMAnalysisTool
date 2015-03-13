__author__ = 'Michael Redmond'

import vtk

from ..custom_pickers import vtkThruCellPicker2


class ThruCellPickerFilter(vtk.vtkProgrammableFilter):
    def __init__(self):
        self.SetExecuteMethod(self.execute)

        self.cell_picker = vtkThruCellPicker2()
        self.cell_picker.SetTolerance(0.005)

    def execute(self):
        self.cell_picker.set_data_set(self.GetInput())
        self.GetOutput().ShallowCopy(self.cell_picker.GetClosestCell())