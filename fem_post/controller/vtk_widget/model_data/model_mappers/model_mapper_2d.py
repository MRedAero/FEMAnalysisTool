__author__ = 'Michael Redmond'

import vtk


class ModelMapper2D(object):
    def __init__(self, input_filter):
        super(ModelMapper2D, self).__init__()

        self.node_geometry = vtk.vtkGeometryFilter()
        self.element_edges = vtk.vtkExtractEdges()
        self.mpc_geometry = vtk.vtkGeometryFilter()

        self.nodes = vtk.vtkPolyDataMapper2D()
        self.elements = vtk.vtkPolyDataMapper2D()
        self.mpcs = vtk.vtkPolyDataMapper2D()

        self.set_input_connection(input_filter)

        self.nodes.SetInputConnection(self.node_geometry.GetOutputPort())
        self.elements.SetInputConnection(self.element_edges.GetOutputPort())
        self.mpcs.SetInputConnection(self.mpc_geometry.GetOutputPort())

        self.coordinate = vtk.vtkCoordinate()
        self.coordinate.SetCoordinateSystem(5)

        self.nodes.SetTransformCoordinate(self.coordinate)
        self.elements.SetTransformCoordinate(self.coordinate)
        self.mpcs.SetTransformCoordinate(self.coordinate)

        self.input_filter = None

    def set_input_connection(self, input_filter):

        self.input_filter = input_filter

        self.node_geometry.SetInputConnection(input_filter.nodes.GetOutputPort())
        self.element_edges.SetInputConnection(input_filter.elements.GetOutputPort())
        self.mpc_geometry.SetInputConnection(input_filter.mpcs.GetOutputPort())

        self.update()

    def update(self):
        self.node_geometry.Update()
        self.element_edges.Update()
        self.mpc_geometry.Update()

        self.node_geometry.Modified()
        self.element_edges.Modified()
        self.mpc_geometry.Modified()

        self.nodes.Update()
        self.elements.Update()
        self.mpcs.Update()

        self.nodes.Modified()
        self.elements.Modified()
        self.mpcs.Modified()