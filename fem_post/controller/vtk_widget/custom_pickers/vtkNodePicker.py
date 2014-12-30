__author__ = 'Michael Redmond'


import vtk

from ..utilities import project_point_from_screen
from ..vtk_globals import *


class vtkNodePointPicker(vtk.vtkPointPicker):
    def __init__(self):

        self.Renderer = None
        self.poly_data = vtk.vtkPolyData()
        self.points = vtk.vtkPoints()
        self.vertex = vtk.vtkVertex()
        self.cells = vtk.vtkCellArray()

        self.PickFromListOn()

    def GetProjectedPoint(self):

        if self.GetPointId() == -1:
            return

        #self.points.Reset()
        #self.poly_data.Reset()
        self.cells = vtk.vtkCellArray()

        p = self.GetDataSet().GetPoint(self.GetPointId())

        worldCoords = project_point_from_screen(p, self.Renderer, 0.001)

        self.points.InsertPoint(0, worldCoords[:3])

        self.poly_data.SetPoints(self.points)

        ids = self.vertex.GetPointIds()
        ids.SetId(0, 0)

        self.cells.InsertCellPoint(0)
        self.cells.InsertNextCell(self.vertex)
        self.poly_data.SetVerts(self.cells)

        return self.poly_data

    def add_pick_list(self, actor):
        self.InitializePickList()
        self.AddPickList(actor)


class vtkNodeCellPicker(vtk.vtkCellPicker):
    def __init__(self):

        self.Renderer = None
        self.poly_data = vtk.vtkPolyData()
        self.points = vtk.vtkPoints()
        self.vertex = vtk.vtkVertex()
        self.cells = vtk.vtkCellArray()

        self.PickFromListOn()

        self.cells_to_pick_from = [0]*10
        self.cells_to_pick_from[VTK_VERTEX] = 1

    def set_picking(self, index, value):
        self.cells_to_pick_from[index] = value

    def GetProjectedPoint(self):

        if self.GetCellId() == -1:
            return

        if not self.cells_to_pick_from[VTK_VERTEX]:
            self.poly_data.Reset()
            return self.poly_data

        #self.points.Reset()
        #self.poly_data.Reset()
        self.cells = vtk.vtkCellArray()

        data_set = self.GetDataSet()

        pid = data_set.GetCell(self.GetCellId()).GetPointId(0)

        p = data_set.GetPoint(pid)

        worldCoords = project_point_from_screen(p, self.Renderer, 0.001)

        self.points.InsertPoint(0, worldCoords[:3])

        self.poly_data.SetPoints(self.points)

        ids = self.vertex.GetPointIds()
        ids.SetId(0, 0)

        self.cells.InsertCellPoint(0)
        self.cells.InsertNextCell(self.vertex)
        self.poly_data.SetVerts(self.cells)

        return self.poly_data

    def add_pick_list(self, actor):
        self.InitializePickList()
        self.AddPickList(actor)