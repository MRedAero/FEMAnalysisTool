__author__ = 'Michael Redmond'

import vtk


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


