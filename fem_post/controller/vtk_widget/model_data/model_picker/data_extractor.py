__author__ = 'Michael Redmond'

import vtk

from ...vtk_globals import *


class DataExtractor(object):
    """This is a helper class for ModelPicker"""

    def __init__(self):
        super(DataExtractor, self).__init__()

        self.input_data = None
        self.implicit_function = None

        self.extractor = vtk.vtkExtractGeometry()
        self.extractor.ExtractInsideOn()
        self.extractor.ExtractBoundaryCellsOn()

    def set_input_data(self, data):
        self.input_data = data

        if VTK_VERSION >= 6.0:
            self.extractor.SetInputData(self.input_data)
        else:
            self.extractor.SetInput(self.input_data)

        if self.implicit_function is not None:
            self.extractor.Update()

    def set_implicit_function(self, implicit_function):
        self.implicit_function = implicit_function

        self.extractor.SetImplicitFunction(self.implicit_function)

        if self.input_data is not None:
            self.extractor.Update()

    def get_output(self):
        return self.extractor.GetOutput()

    def update(self):
        if self.input_data is not None and self.implicit_function is not None:
            self.extractor.Update()