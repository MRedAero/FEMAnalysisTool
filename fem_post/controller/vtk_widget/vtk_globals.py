__author__ = 'Michael Redmond'

import vtk

VTK_VERSION = vtk.vtkVersion().GetVTKMajorVersion()

VTK_VERTEX = 1
VTK_LINE = 3
VTK_POLY_LINE = 4
VTK_TRI = 5
VTK_QUAD = 9

SELECTION_REPLACE = 0
SELECTION_APPEND = 1
SELECTION_REMOVE = 2

SELECTION_SINGLE = 0
SELECTION_BOX = 1
SELECTION_POLY = 2

a = vtk.util.vtkAlgorithm.VTKPythonAlgorithmBase()