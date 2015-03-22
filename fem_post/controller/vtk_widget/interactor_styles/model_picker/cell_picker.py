__author__ = 'Michael Redmond'


import vtk
from vtk.vtkCommonCorePython import mutable
from ...utilities import *
from ...vtk_globals import vtk_globals


class CellPicker(vtk.vtkCellLocator):

    def __init__(self):
        self.Renderer = None
        self.PickPosition = [0, 0, 0]
        self.Tolerance = 0.005
        self.p1World = [0, 0, 0, 0]
        self.p2World = [0, 0, 0, 0]
        self.ids = vtk.vtkIdList()
        self.ClosestCellId = -1
        self.ClosestCellGlobalId = -1

        self.id_array = vtk.vtkIdTypeArray()
        self.id_array.SetNumberOfComponents(1)

        self.global_id_array = vtk.vtkIdTypeArray()
        self.global_id_array.SetNumberOfComponents(1)

        self.cells_to_pick_from = [0]*10
        self.cells_to_pick_from[vtk_globals.VTK_NODE] = 1
        self.cells_to_pick_from[vtk_globals.VTK_VERTEX] = 1
        self.cells_to_pick_from[vtk_globals.VTK_LINE] = 1
        self.cells_to_pick_from[vtk_globals.VTK_TRI] = 1
        self.cells_to_pick_from[vtk_globals.VTK_QUAD] = 1
        self.cells_to_pick_from[vtk_globals.VTK_POLY_LINE] = 1

    def set_picking(self, index, value):
        self.cells_to_pick_from[index] = value

    def SetTolerance(self, value):
        self.Tolerance = value

    def Pick(self, selectionX, selectionY, selectionZ, renderer=None):

        self.ids.Reset()

        if renderer is None:
            print "Renderer has not been set!"
            return

        self.Renderer = renderer

        ray_result = picking_ray([selectionX, selectionY, selectionZ], renderer)

        if ray_result != -1:
            self.selection_point = ray_result[0]
            self.PickPosition = ray_result[1]
            self.p1World = ray_result[2]
            self.p2World = ray_result[3]
        else:
            return

        tol = self.Tolerance

        self.FindCellsAlongLine(self.p1World[:3], self.p2World[:3], tol, self.ids)

        self.ClosestCellId = -1
        self.ClosestCellGlobalId = -1

        # determine which cells are actually intersected

        data = self.GetDataSet()

        global_ids = data.GetCellData().GetGlobalIds()

        self.id_array.Reset()
        self.global_id_array.Reset()

        self.id_list = []
        self.global_id_list = []

        t = mutable(0.)
        x = [0, 0, 0]
        pcoords = [0, 0, 0]
        subId = mutable(0)

        OFFSET_ELEMENT = vtk_globals.OFFSET_ELEMENT

        my_int = int

        for i in xrange(self.ids.GetNumberOfIds()):
            id = self.ids.GetId(i)
            cell = data.GetCell(id)

            try:
                if not self.cells_to_pick_from[cell.GetCellType()]:
                    continue
            except IndexError:
                continue

            nodes_exist = False

            if cell.IntersectWithLine(self.p1World[:3], self.p2World[:3], tol, t, x, pcoords, subId):
                self.id_array.InsertNextValue(id)
                self.id_list.append(id)

                global_id = my_int(global_ids.GetTuple(id)[0])
                self.global_id_list.append(global_id)
                self.global_id_array.InsertNextValue(global_id)

                #print global_id

                if global_id < OFFSET_ELEMENT:
                    nodes_exist = True

            if nodes_exist:
                new_id_array = vtk.vtkIdTypeArray()
                new_id_array.ShallowCopy(self.id_array)

                new_global_id_array = vtk.vtkIdTypeArray()
                new_global_id_array.ShallowCopy(self.global_id_array)

                for i in xrange(self.id_array.GetNumberOfTuples()):
                    global_id = my_int(self.global_id_array.GetTuple(i)[0])
                    id = my_int(self.id_array.GetTuple(i)[0])

                    if global_id < OFFSET_ELEMENT:
                        new_global_id_array.InsertNextValue(global_id)
                        new_id_array.InsertNextValue(id)

                new_global_id_array.Squeeze()
                new_id_array.Squeeze()

                self.id_array.Reset()
                self.global_id_array.Reset()

                self.id_array.ShallowCopy(new_id_array)
                self.global_id_array.ShallowCopy(new_global_id_array)
            else:
                self.id_array.Squeeze()
                self.global_id_array.Squeeze()

        self.update_ids()

    def GetCellIds(self):
        return self.id_array

    def update_ids(self):
        if self.ClosestCellId != -1:
            return

        selectionNode = vtk.vtkSelectionNode()
        selectionNode.SetFieldType(vtk.vtkSelectionNode.CELL)
        selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
        selectionNode.SetSelectionList(self.id_array)

        selection = vtk.vtkSelection()
        selection.AddNode(selectionNode)

        extractSelection = vtk.vtkExtractSelection()
        extractSelection.SetInputData(0, self.GetDataSet())
        extractSelection.SetInputData(1, selection)
        extractSelection.Update()

        cc = vtk.vtkCellCenters()
        cc.VertexCellsOff()
        cc.SetInputData(extractSelection.GetOutput())
        cc.Update()

        poly_data = cc.GetOutput()

        min_d = 999999999.

        line = vtk.vtkLine()

        min_i = -1

        self.p_min = None

        #print poly_data.GetNumberOfPoints()

        for i in xrange(poly_data.GetNumberOfPoints()):
            p = poly_data.GetPoint(i)
            d = line.DistanceToLine(p, self.p1World[:3], self.p2World[:3])

            if d < min_d:
                min_i = i
                min_d = d
                self.p_min = p

        if min_i >= 0:
            self.ClosestCellId = self.id_list[min_i]
            self.ClosestCellGlobalId = self.global_id_list[min_i]

    def GetClosestCellId(self):
        return self.ClosestCellId

    def GetClosestCellGlobalId(self):
        return self.ClosestCellGlobalId