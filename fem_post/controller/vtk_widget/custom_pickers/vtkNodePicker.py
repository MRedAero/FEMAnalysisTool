__author__ = 'Michael Redmond'


import vtk


class vtkNodePicker(vtk.vtkPointPicker):
    def __init__(self):

        self.Renderer = None
        self.poly_data = vtk.vtkPolyData()
        self.points = vtk.vtkPoints()
        self.vertex = vtk.vtkVertex()
        self.cells = vtk.vtkCellArray()

    def GetProjectedPoint(self):

        if self.GetPointId() == -1:
            return

        #self.points.Reset()
        #self.poly_data.Reset()
        self.cells = vtk.vtkCellArray()

        p = self.GetDataSet().GetPoint(self.GetPointId())

        self.Renderer.SetWorldPoint(p[0], p[1], p[2], 1.)
        self.Renderer.WorldToDisplay()
        displayCoords = self.Renderer.GetDisplayPoint()

        self.Renderer.SetDisplayPoint(displayCoords[0], displayCoords[1], 0.001)
        self.Renderer.DisplayToWorld()
        worldCoords = self.Renderer.GetWorldPoint()

        self.points.InsertPoint(0, worldCoords[:3])

        self.poly_data.SetPoints(self.points)

        ids = self.vertex.GetPointIds()
        ids.SetId(0, 0)

        self.cells.InsertCellPoint(0)
        self.cells.InsertNextCell(self.vertex)
        self.poly_data.SetVerts(self.cells)

        return self.poly_data