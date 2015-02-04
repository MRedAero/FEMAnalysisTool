__author__ = 'Michael Redmond'

import vtk

from ..vtk_globals import *


def project_cell_from_screen(cell, points, renderer, dist):
    cell_type = cell.GetCellType()

    point_ids = cell.GetPointIds()

    id_count = point_ids.GetNumberOfIds()

    if id_count == 0:
        return None

    if cell_type == 1:
        pos = points.GetPoint(point_ids[0])

        new_pos = project_point_from_screen(pos, renderer, dist)

        new_cell = vtk.vtkVertex


def project_point_from_screen(pos, renderer, dist):
    """

    :param pos: list
    :param renderer: vtk.vtkRenderer
    :param dist: float
    :return: list
    """

    renderer.SetWorldPoint(pos[0], pos[1], pos[2], 1.)
    renderer.WorldToDisplay()
    displayCoords = renderer.GetDisplayPoint()

    renderer.SetDisplayPoint(displayCoords[0], displayCoords[1], dist)
    renderer.DisplayToWorld()

    return renderer.GetWorldPoint()


def display_to_world(pos, renderer, dist):
    """

    :param pos: list
    :param renderer: vtk.vtkRenderer
    :param dist: float
    :return: list
    """

    renderer.SetDisplayPoint(pos[0], pos[1], dist)
    renderer.DisplayToWorld()

    return renderer.GetWorldPoint()


def picking_ray(pos, renderer):
    """

    :param pos: list
    :param renderer: vtk.vtkRenderer
    :return:
    """

    selectionX = pos[0]
    selectionY = pos[1]
    selectionZ = pos[2]

    # code below is adapted from vtkPicker::Pick to calculate ray end points

    # Initialize picking process
    selection_point = [selectionX, selectionY, selectionZ]

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
        return -1

    PickPosition = [0, 0, 0]

    for i in xrange(3):
        PickPosition[i] = worldCoords[i]/worldCoords[3]

    # Compute the ray endpoints.  The ray is along the line running from
    # the camera position to the selection point, starting where this line
    # intersects the front clipping plane, and terminating where this
    # line intersects the back clipping plane.

    ray = [0, 0, 0]
    cameraDOP = [0, 0, 0]

    magnitude = 0.

    for i in xrange(3):
        ray[i] = PickPosition[i] - cameraPos[i]
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

    p1World = [0, 0, 0, 0]
    p2World = [0, 0, 0, 0]

    if camera.GetParallelProjection():
        tF = clipRange[0] - rayLength
        tB = clipRange[1] - rayLength
        for i in xrange(3):
            p1World[i] = PickPosition[i] + tF*cameraDOP[i]
            p2World[i] = PickPosition[i] + tB*cameraDOP[i]
    else:
        tF = clipRange[0]/rayLength
        tB = clipRange[1]/rayLength
        for i in xrange(3):
            p1World[i] = cameraPos[i] + tF*ray[i]
            p2World[i] = cameraPos[i] + tB*ray[i]

    p1World[3] = p2World[3] = 1.

    return [selection_point, PickPosition, p1World, p2World]


def len_between_points(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]

    return (dx**2 + dy**2 + dz**2)**0.5


def vector_between_points(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]

    len = (dx**2 + dy**2 + dz**2)**0.5

    if len == 0:
        return [0, 0, 0]
    else:
        return [dx/len, dy/len, dz/len]


def points_to_poly_data(poly_data, points, cells):

    poly_data = poly_data['poly_data']

    point_list = vtk.vtkPoints()

    for i in xrange(len(points)):
        point_list.InsertNextPoint(points[i][0], points[i][1], points[i][2])

    cell_array = vtk.vtkCellArray()

    for i in xrange(len(cells)):
        pts = cells[i]

        if len(pts) == 1:
            cell = vtk.vtkVertex()
            ids = cell.GetPointIds()
            ids.SetId(0, pts[0])
        if len(pts) == 2:
            cell = vtk.vtkLine()
            ids = cell.GetPointIds()
            ids.SetId(0, pts[0])
            ids.SetId(1, pts[1])
        elif len(pts) == 3:
            cell = vtk.vtkTriangle()
            ids = cell.GetPointIds()
            ids.SetId(0, pts[0])
            ids.SetId(1, pts[1])
            ids.SetId(2, pts[2])
        elif len(pts) == 4:
            cell = vtk.vtkQuad()
            ids = cell.GetPointIds()
            ids.SetId(0, pts[0])
            ids.SetId(1, pts[1])
            ids.SetId(2, pts[2])
            ids.SetId(3, pts[3])
        else:
            continue

        cell_array.InsertNextCell(cell)

    poly_data.Reset()

    poly_data.SetPoints(point_list)
    poly_data.SetVerts(cell_array)
    poly_data.SetLines(cell_array)
    poly_data.SetPolys(cell_array)


def create_box_frustum(x0_, y0_, x1_, y1_, renderer):

    if x0_ < x1_:
        x0 = x0_
        x1 = x1_
    else:
        x0 = x1_
        x1 = x0_

    if y0_ < y1_:
        y0 = y0_
        y1 = y1_
    else:
        y0 = y1_
        y1 = y0_

    if x0 == x1:
        x1 += 1.

    if y0 == y1:
        y1 += 1.

    verts = []

    renderer.SetDisplayPoint(x0, y0, 0)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    renderer.SetDisplayPoint(x0, y0, 1)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    renderer.SetDisplayPoint(x0, y1, 0)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    renderer.SetDisplayPoint(x0, y1, 1)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    renderer.SetDisplayPoint(x1, y0, 0)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    renderer.SetDisplayPoint(x1, y0, 1)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    renderer.SetDisplayPoint(x1, y1, 0)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    renderer.SetDisplayPoint(x1, y1, 1)
    renderer.DisplayToWorld()
    verts.extend(renderer.GetWorldPoint()[:4])

    extract_selected_frustum = vtk.vtkExtractSelectedFrustum()
    extract_selected_frustum.CreateFrustum(verts)

    return extract_selected_frustum.GetFrustum()