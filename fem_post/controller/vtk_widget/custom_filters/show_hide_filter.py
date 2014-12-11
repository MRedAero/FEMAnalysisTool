__author__ = 'Michael Redmond'

import vtk

from ..custom_data import CustomUnstructuredGrid


class ShowHideFilter(vtk.vtkProgrammableFilter):
    def __init__(self):
        self.SetExecuteMethod(self.execute)

        self.input = None
        self.shown = CustomUnstructuredGrid()
        self.hidden = CustomUnstructuredGrid()
        self.widget = None

        self.show = True

    def execute(self):

        if self.input is None:
            return

        input = self.input.data
        visible = self.input.visible

        self.shown.data.Reset()
        self.shown.map = []

        self.hidden.data.Reset()
        self.hidden.map = []

        self.shown.data.SetPoints(input.GetPoints())
        self.hidden.data.SetPoints(input.GetPoints())

        for i in xrange(input.GetNumberOfCells()):
            cell = input.GetCell(i)

            if visible[i]:
                self.shown.data.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
                self.shown.map.append(i)
            else:
                self.hidden.data.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
                self.hidden.map.append(i)

        self.shown.data.Modified()
        self.hidden.data.Modified()
        self.widget.screen_update()