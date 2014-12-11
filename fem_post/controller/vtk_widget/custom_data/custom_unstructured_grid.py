__author__ = 'Michael Redmond'

import vtk


class CustomUnstructuredGrid(object):
    def __init__(self):
        super(CustomUnstructuredGrid, self).__init__()

        self.data = vtk.vtkUnstructuredGrid()
        self.visible = []
        self.map = []