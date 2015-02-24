__author__ = 'Michael Redmond'


import vtk

from ..vtk_globals import vtk_globals


class VertexPicker(vtk.vtkCellPicker):
    def __init__(self):
        self.PickFromListOn()

    def GetCellGlobalId(self):
        id_ = self.GetCellId()

        if id_ == -1:
            return -1

        data = self.GetDataSet()

        global_ids = data.GetCellData().GetGlobalIds()

        return int(global_ids.GetTuple(id_)[0])