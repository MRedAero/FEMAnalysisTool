__author__ = 'Michael Redmond'


import vtk


class vtkThruCellPicker(vtk.vtkCellLocator):
    def __init__(self):
        self.Renderer = None
        self.PickPosition = [0, 0, 0]
        self.Tolerance = 0.005
        self.p1World = [0, 0, 0, 0]
        self.p2World = [0, 0, 0, 0]
        self.ids = vtk.vtkIdList()
        self.ClosestCellId = -1

    def SetTolerance(self, value):
        self.Tolerance = value

    def Pick(self, selectionX, selectionY, selectionZ, renderer=None):

        self.ids.Reset()

        if renderer is None:
            print "Renderer has not been set!"
            return

        self.Renderer = renderer

        # code below is adapted from vtkPicker::Pick to calculate ray end points

        # Initialize picking process
        self.selection_point = [selectionX, selectionY, selectionZ]

        # Get camera focal point and position. Convert to display (screen)
        # coordinates. We need a depth value for z-buffer.
        camera = renderer.GetActiveCamera()
        cameraPos = camera.GetPosition()
        cameraPos += (1.,)
        cameraFP = camera.GetFocalPoint()
        cameraFP += (1.,)

        renderer.SetWorldPoint(cameraFP[0], cameraFP[1], cameraFP[2], cameraFP[3])
        renderer.WorldToDisplay()
        displayCoords = renderer.GetDisplayPoint()
        selectionZ = displayCoords[2]

        # Convert the selection point into world coordinates.
        renderer.SetDisplayPoint(selectionX, selectionY, selectionZ)
        renderer.DisplayToWorld()
        worldCoords = renderer.GetWorldPoint()

        if worldCoords[3] == 0.:
            print "Bad homogeneous coordinates"
            return

        for i in xrange(3):
            self.PickPosition[i] = worldCoords[i]/worldCoords[3]

        # Compute the ray endpoints.  The ray is along the line running from
        # the camera position to the selection point, starting where this line
        # intersects the front clipping plane, and terminating where this
        # line intersects the back clipping plane.

        ray = [0, 0, 0]
        cameraDOP = [0, 0, 0]

        magnitude = 0.

        for i in xrange(3):
            ray[i] = self.PickPosition[i] - cameraPos[i]
            cameraDOP[i] = cameraFP[i] - cameraPos[i]
            magnitude += cameraDOP[i]**2

        magnitude **= 0.5

        for i in xrange(3):
            cameraDOP[i] /= magnitude

        dot_product = cameraDOP[0]*ray[0] + cameraDOP[1]*ray[1] + cameraDOP[2]*ray[2]

        if dot_product == 0.:
            print "Cannot process points"
            return

        rayLength = dot_product

        clipRange = camera.GetClippingRange()

        self.project_base = [0, 0, 0]

        self.project_magnitude = 0.

        if camera.GetParallelProjection():
            tF = clipRange[0] - rayLength
            tB = clipRange[1] - rayLength
            for i in xrange(3):
                self.p1World[i] = self.PickPosition[i] + tF*cameraDOP[i]
                self.p2World[i] = self.PickPosition[i] + tB*cameraDOP[i]
                self.project_base[i] = self.p1World[i] - self.p2World[i]
                self.project_magnitude += self.project_base[i]**2
                self.project_base[i] += self.p1World[i]
        else:
            tF = clipRange[0]/rayLength
            tB = clipRange[1]/rayLength
            for i in xrange(3):
                self.p1World[i] = cameraPos[i] + tF*ray[i]
                self.p2World[i] = cameraPos[i] + tB*ray[i]
                self.project_base[i] = self.p1World[i] - self.p2World[i]
                self.project_magnitude += self.project_base[i]**2
                self.project_base[i] += self.p1World[i]

        self.p1World[3] = self.p2World[3] = 1.

        self.project_magnitude **= 0.5

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

        self.FindCellsAlongLine(self.p1World[:3], self.p2World[:3], tol, self.ids)

        self.ClosestCellId = -1

    def GetCellIds(self):
        return self.ids

    def GetClosestCellId(self):

        if self.ClosestCellId != -1:
            return self.ClosestCellId

        ids = vtk.vtkIdTypeArray()
        ids.SetNumberOfComponents(1)

        for i in xrange(self.ids.GetNumberOfIds()):
            ids.InsertNextValue(self.ids.GetId(i))

        selectionNode = vtk.vtkSelectionNode()
        selectionNode.SetFieldType(vtk.vtkSelectionNode.CELL)
        selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
        selectionNode.SetSelectionList(ids)

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
            self.ClosestCellId = self.ids.GetId(min_i)
            return self.ClosestCellId
        else:
            return -1

    def GetClosestCellEdges(self):

        if self.ClosestCellId == -1:
            return

        cell = self.GetDataSet().GetCell(self.ClosestCellId)

        cell_points = cell.GetPoints()

        distance_to_element = 0.

        for i in xrange(3):
            distance_to_element += (self.project_base[i] - self.p_min[i])**2

        distance_to_element **= 0.5

        factor = self.project_magnitude/distance_to_element

        points = vtk.vtkPoints()

        for i in xrange(cell_points.GetNumberOfPoints()):
            p = cell_points.GetPoint(i)

            p_new = [0, 0, 0]

            for j in xrange(3):
                p_new[j] = self.project_base[j] + (p[j] - self.project_base[j])*factor

            points.InsertNextPoint(p_new)

        poly_data = vtk.vtkPolyData()

        edges = vtk.vtkCellArray()

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

        poly_data.SetPoints(points)
        poly_data.SetLines(edges)

        return poly_data