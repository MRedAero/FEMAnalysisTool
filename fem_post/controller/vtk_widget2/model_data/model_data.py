__author__ = 'Michael Redmond'

import vtk


class ModelBaseData(object):
    def __init__(self):
        super(ModelBaseData, self).__init__()

        self.data = vtk.vtkUnstructuredGrid()

        self.points = None

        self.global_ids = vtk.vtkIdTypeArray()
        self.global_ids.SetName("global_ids")

        self.visible = vtk.vtkIntArray()
        self.visible.SetName("visible")

        self.original_ids = vtk.vtkIntArray()
        self.original_ids.SetName("original_ids")

        self.basic_types = vtk.vtkIntArray()
        self.basic_types.SetName("basic_types")

        self.basic_shapes = vtk.vtkIntArray()
        self.basic_shapes.SetName("basic_shapes")

        self.data.GetCellData().SetGlobalIds(self.global_ids)
        self.data.GetCellData().AddArray(self.visible)
        self.data.GetCellData().AddArray(self.original_ids)
        self.data.GetCellData().AddArray(self.global_ids)
        self.data.GetCellData().AddArray(self.basic_types)
        self.data.GetCellData().AddArray(self.basic_shapes)

    def set_points(self, points):
        self.points = points
        self.data.SetPoints(points)

    def reset(self):
        self.data.Reset()
        self.global_ids.Reset()
        self.visible.Reset()
        self.original_ids.Reset()

        self.data.GetCellData().SetGlobalIds(self.global_ids)
        self.data.GetCellData().AddArray(self.visible)
        self.data.GetCellData().AddArray(self.original_ids)

        self.points = None

    def squeeze(self):
        self.data.Squeeze()
        self.global_ids.Squeeze()
        self.visible.Squeeze()
        self.original_ids.Squeeze()
        self.basic_types.Squeeze()

    def update(self):
        self.data.Modified()


class ModelDataHelper(object):
    def __init__(self, data):
        super(ModelDataHelper, self).__init__()

        self.data = data

        self.points = vtk.vtkPoints()
        self.data.SetPoints(self.points)

        self.global_ids1 = vtk.vtkIdTypeArray()
        #self.global_ids1.SetName("global_ids")

        self.global_ids2 = vtk.vtkIntArray()
        self.global_ids2.SetName("global_ids")

        self.visible = vtk.vtkIntArray()
        self.visible.SetName("visible")

        self.original_ids = vtk.vtkIntArray()
        self.original_ids.SetName("original_ids")

        self.basic_types = vtk.vtkIntArray()
        self.basic_types.SetName("basic_types")

        self.basic_shapes = vtk.vtkIntArray()
        self.basic_shapes.SetName("basic_shapes")

        self.data.GetCellData().SetGlobalIds(self.global_ids1)
        self.data.GetCellData().AddArray(self.visible)
        self.data.GetCellData().AddArray(self.original_ids)
        self.data.GetCellData().AddArray(self.global_ids2)
        self.data.GetCellData().AddArray(self.basic_types)
        self.data.GetCellData().AddArray(self.basic_shapes)

    def set_points(self, points):
        self.points = points
        self.data.SetPoints(points)

    def reset(self):
        self.data.Reset()
        self.global_ids1.Reset()
        self.visible.Reset()
        self.original_ids.Reset()
        self.basic_types.Reset()
        self.basic_shapes.Reset()

        self.data.GetCellData().SetGlobalIds(self.global_ids1)
        self.data.GetCellData().AddArray(self.visible)
        self.data.GetCellData().AddArray(self.original_ids)
        self.data.GetCellData().AddArray(self.global_ids1)
        self.data.GetCellData().AddArray(self.basic_types)
        self.data.GetCellData().AddArray(self.basic_shapes)

        self.points = None

    def squeeze(self):
        self.data.Squeeze()
        self.global_ids1.Squeeze()
        self.visible.Squeeze()
        self.original_ids.Squeeze()
        self.basic_types.Squeeze()
        self.basic_shapes.Squeeze()

    def update(self):
        self.data.Modified()


