__author__ = 'Michael Redmond'

import vtk


class ModelGroupFilterBase(vtk.vtkProgrammableFilter):
    def __init__(self):
        self.SetExecuteMethod(self.execute)

    def execute(self):
        self.GetOutput().ShallowCopy(self.GetInput())
        self.Modified()


class ModelGroupFilter(object):
    def __init__(self):

        self.nodes = ModelGroupFilterBase()
        self.elements = ModelGroupFilterBase()
        self.mpcs = ModelGroupFilterBase()

        self.input_data = None
        self.input_filter = None

    def set_input_data(self, input_data):
        """

        @type data: fem_post.controller.vtk_widget.model_data.model_data.ModelData2
        """

        self.input_data = input_data
        self.input_filter = None

        self.nodes.SetInputData(input_data.nodes.data)
        self.elements.SetInputData(input_data.elements.data)
        self.mpcs.SetInputData(input_data.mpcs.data)

        self.update()

    def set_input_connection(self, input_filter):

        self.input_filter = input_filter
        self.input_data = None

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