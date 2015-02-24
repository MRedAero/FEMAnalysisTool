__author__ = 'Michael Redmond'


import vtk
from vtk.vtkCommonCorePython import mutable
from ..utilities import *
from ..vtk_globals import *
from ..model_data.model_filters import ModelExtractSelectionFilterBase


class vtkThruCellPicker(vtk.vtkCellLocator):

    def __init__(self):
        self.Renderer = None
        self.PickPosition = [0, 0, 0]
        self.Tolerance = 0.005
        self.p1World = [0, 0, 0, 0]
        self.p2World = [0, 0, 0, 0]
        self.ids = vtk.vtkIdList()
        self.ClosestCellId = -1

        self.edges = vtk.vtkPolyData()

        self.cells_to_pick_from = [0]*10
        self.cells_to_pick_from[VTK_VERTEX] = 1
        self.cells_to_pick_from[VTK_LINE] = 1
        self.cells_to_pick_from[VTK_TRI] = 1
        self.cells_to_pick_from[VTK_QUAD] = 1
        self.cells_to_pick_from[VTK_POLY_LINE] = 1

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

        if 0:
            # Compute the tolerance in world coordinates.  Do this by
            # determining the world coordinates of the diagonal points of the
            # window, computing the width of the window in world coordinates, and
            # multiplying by the tolerance.

            viewport = renderer.GetViewport()
            if renderer.GetRenderWindow():
                winSizePtr = renderer.GetRenderWindow().GetSize()
                winSize = [winSizePtr[0], winSizePtr[1]]

            x = winSize[0]*viewport[0]
            y = winSize[1]*viewport[1]
            renderer.SetDisplayPoint(x, y, selectionZ)
            renderer.DisplayToWorld()
            windowLowerLeft = renderer.GetWorldPoint()

            x = winSize[0]*viewport[2]
            y = winSize[1]*viewport[3]
            renderer.SetDisplayPoint(x, y, selectionZ)
            renderer.DisplayToWorld()
            windowUpperRight = renderer.GetWorldPoint()

            tol = 0.
            for i in xrange(3):
                tol += (windowUpperRight[i] - windowLowerLeft[i])**2

            tol = self.Tolerance*tol**0.5

        tol = self.Tolerance

        self.FindCellsAlongLine(self.p1World[:3], self.p2World[:3], tol, self.ids)

        self.ClosestCellId = -1

        # determine which cells are actually intersected

        data = self.GetDataSet()

        self.id_array = vtk.vtkIdTypeArray()
        self.id_array.SetNumberOfComponents(1)

        self.id_list = []

        t = mutable(0.)
        x = [0, 0, 0]
        pcoords = [0, 0, 0]
        subId = mutable(0)

        for i in xrange(self.ids.GetNumberOfIds()):
            id = self.ids.GetId(i)
            cell = data.GetCell(id)

            try:
                if not self.cells_to_pick_from[cell.GetCellType()]:
                    continue
            except IndexError:
                continue

            if cell.IntersectWithLine(self.p1World[:3], self.p2World[:3], tol, t, x, pcoords, subId):
                self.id_array.InsertNextValue(id)
                self.id_list.append(id)
            #else:
            #    print 'cell %d does not intersect' % id

    def GetCellIds(self):
        return self.id_array

    def GetClosestCellId(self):

        if self.ClosestCellId != -1:
            return self.ClosestCellId

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

        for i in xrange(poly_data.GetNumberOfPoints()):
            p = poly_data.GetPoint(i)
            d = line.DistanceToLine(p, self.p1World[:3], self.p2World[:3])

            if d < min_d:
                min_i = i
                min_d = d
                self.p_min = p

        if min_i >= 0:
            self.ClosestCellId = self.id_list[min_i]
            return self.ClosestCellId
        else:
            return -1

    def GetClosestCellEdges(self):

        self.edges.Reset()

        if self.ClosestCellId == -1:
            return self.edges

        cell = self.GetDataSet().GetCell(self.ClosestCellId)

        cell_points = cell.GetPoints()

        points = vtk.vtkPoints()

        edges = vtk.vtkCellArray()

        for i in xrange(cell_points.GetNumberOfPoints()):
            p = cell_points.GetPoint(i)

            worldCoords = project_point_from_screen(p, self.Renderer, 0.001)

            points.InsertNextPoint(worldCoords[:3])

        self.edges.SetPoints(points)

        if cell_points.GetNumberOfPoints() > 1:
            for i in xrange(cell_points.GetNumberOfPoints()-1):
                cell = vtk.vtkLine()
                ids = cell.GetPointIds()
                ids.SetId(0, i)
                ids.SetId(1, i+1)
                edges.InsertNextCell(cell)

            cell = vtk.vtkLine()
            ids = cell.GetPointIds()
            ids.SetId(0, i+1)
            ids.SetId(1, 0)
            edges.InsertNextCell(cell)

            self.edges.SetLines(edges)
        else:
            cell = vtk.vtkVertex()
            ids = cell.GetPointIds()
            ids.SetId(0, 0)
            edges.InsertNextCell(cell)
            self.edges.SetVertices(edges)

        return self.edges


class vtkThruCellPicker2(vtk.vtkCellLocator):

    def __init__(self):
        self.Renderer = None
        self.PickPosition = [0, 0, 0]
        self.Tolerance = 0.005
        self.p1World = [0, 0, 0, 0]
        self.p2World = [0, 0, 0, 0]
        self.ids = vtk.vtkIdList()
        self.ClosestCellId = -1

        self.closest_cell_filter = ModelExtractSelectionFilterBase()

        self.cells_to_pick_from = [0]*10
        self.cells_to_pick_from[VTK_VERTEX] = 1
        self.cells_to_pick_from[VTK_LINE] = 1
        self.cells_to_pick_from[VTK_TRI] = 1
        self.cells_to_pick_from[VTK_QUAD] = 1
        self.cells_to_pick_from[VTK_POLY_LINE] = 1

    def set_picking(self, index, value):
        self.cells_to_pick_from[index] = value

    def set_data_set(self, data_set):
        self.SetDataSet(data_set)
        self.closest_cell_filter.set_input_data(data_set, True)

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

        if 0:
            # Compute the tolerance in world coordinates.  Do this by
            # determining the world coordinates of the diagonal points of the
            # window, computing the width of the window in world coordinates, and
            # multiplying by the tolerance.

            viewport = renderer.GetViewport()
            if renderer.GetRenderWindow():
                winSizePtr = renderer.GetRenderWindow().GetSize()
                winSize = [winSizePtr[0], winSizePtr[1]]

            x = winSize[0]*viewport[0]
            y = winSize[1]*viewport[1]
            renderer.SetDisplayPoint(x, y, selectionZ)
            renderer.DisplayToWorld()
            windowLowerLeft = renderer.GetWorldPoint()

            x = winSize[0]*viewport[2]
            y = winSize[1]*viewport[3]
            renderer.SetDisplayPoint(x, y, selectionZ)
            renderer.DisplayToWorld()
            windowUpperRight = renderer.GetWorldPoint()

            tol = 0.
            for i in xrange(3):
                tol += (windowUpperRight[i] - windowLowerLeft[i])**2

            tol = self.Tolerance*tol**0.5

        tol = self.Tolerance

        self.FindCellsAlongLine(self.p1World[:3], self.p2World[:3], tol, self.ids)

        self.ClosestCellId = -1

        # determine which cells are actually intersected

        data = self.GetDataSet()

        self.id_array = vtk.vtkIdTypeArray()
        self.id_array.SetNumberOfComponents(1)

        self.id_list = []

        t = mutable(0.)
        x = [0, 0, 0]
        pcoords = [0, 0, 0]
        subId = mutable(0)

        for i in xrange(self.ids.GetNumberOfIds()):
            id = self.ids.GetId(i)
            cell = data.GetCell(id)

            try:
                if not self.cells_to_pick_from[cell.GetCellType()]:
                    continue
            except IndexError:
                continue

            if cell.IntersectWithLine(self.p1World[:3], self.p2World[:3], tol, t, x, pcoords, subId):
                self.id_array.InsertNextValue(id)
                self.id_list.append(id)
                #else:
                #    print 'cell %d does not intersect' % id

    def GetCellIds(self):
        return self.id_array

    def GetClosestCellId(self):

        if self.ClosestCellId != -1:
            return self.ClosestCellId

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

        for i in xrange(poly_data.GetNumberOfPoints()):
            p = poly_data.GetPoint(i)
            d = line.DistanceToLine(p, self.p1World[:3], self.p2World[:3])

            if d < min_d:
                min_i = i
                min_d = d
                self.p_min = p

        if min_i >= 0:
            self.ClosestCellId = self.id_list[min_i]
            return self.ClosestCellId
        else:
            return -1

    def GetClosestCell(self):

        if self.ClosestCellId == -1:
            self.closest_cell_filter.reset()
            self.closest_cell_filter.GetOutput()

        self.closest_cell_filter.set_selection_list([self.ClosestCellId])

        return self.closest_cell_filter.GetOutput()