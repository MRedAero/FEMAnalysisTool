__author__ = 'Michael Redmond'

import vtk


class ModelMapper(object):
    def __init__(self):
        super(ModelMapper, self).__init__()

        self.nodes = vtk.vtkDataSetMapper()
        self.elements = vtk.vtkDataSetMapper()
        self.mpcs = vtk.vtkDataSetMapper()

        self.input_filter = None

    def set_input_connection(self, input_filter):

        self.input_filter = input_filter

        self.nodes.SetInputConnection(input_filter.nodes.GetOutputPort())
        self.elements.SetInputConnection(input_filter.elements.GetOutputPort())
        self.mpcs.SetInputConnection(input_filter.mpcs.GetOutputPort())

        self.update()

    def update(self):
        self.nodes.Update()
        self.elements.Update()
        self.mpcs.Update()

        self.nodes.Modified()
        self.elements.Modified()
        self.mpcs.Modified()