__author__ = 'Michael Redmond'

from collections import OrderedDict

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase


class AbstractSplitDataFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
                                        nInputPorts=1, inputType='vtkUnstructuredGrid',
                                        nOutputPorts=1, outputType='vtkUnstructuredGrid')

        self.selection_node = vtk.vtkSelectionNode()
        self.selection = vtk.vtkSelection()
        self.ex = vtk.vtkExtractSelection()
        self.ex.ReleaseDataFlagOn()

        self.selection_node.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)
        self.selection.AddNode(self.selection_node)
        self.ex.SetInputDataObject(1, self.selection)

        self._category_selections = OrderedDict()

    def add_category(self, category_name, category_selection):
        assert isinstance(category_name, str)
        assert isinstance(category_selection, vtk.vtkIntArray)

        self._category_selections[category_name] = category_selection

        self.SetNumberOfOutputPorts(len(self._category_selections.keys()))

        self.Modified()

    def remove_category(self, category_name):
        # let an error pop up for now if the key isn't found, useful for debugging
        del self._category_selections[category_name]

        self.SetNumberOfOutputPorts(len(self._category_selections.keys()))

        self.Modified()

    def RequestData(self, request, inInfo, outInfo):

        inp = vtk.vtkUnstructuredGrid.GetData(inInfo[0])

        if inp is None or inp.GetNumberOfCells() == 0:
            return 1

        self.ex.SetInputDataObject(0, inp)

        GetData = vtk.vtkUnstructuredGrid.GetData
        GetInformationObject = outInfo.GetInformationObject
        selection_node = self.selection_node
        SetSelectionList = selection_node.SetSelectionList
        selection_node_Modified = selection_node.Modified
        selection_Modified = self.selection.Modified
        ex_Modified = self.ex.Modified
        ex_Update = self.ex.Update
        GetOutput = self.ex.GetOutput

        categories = self._category_selections

        i = 0
        for category in categories.keys():
            opt = GetData(GetInformationObject(i))
            SetSelectionList(categories[category])
            selection_node_Modified()
            selection_Modified()
            ex_Modified()
            ex_Update()
            new_output = GetOutput()
            opt.ShallowCopy(new_output)

            i += 1

        return 1

    def get_output_port_by_name(self, name):
        index = self._category_selections.keys().index(name)
        return self.GetOutputPort(index)

    def get_output_port_by_index(self, index):
        return self.GetOutputPort(index)

    def get_output_data_by_name(self, name):
        index = self._category_selections.keys().index(name)
        return self.GetOutputDataObject(index)

    def get_output_data_by_index(self, index):
        return self.GetOutputDataObject(index)

    def get_categories(self):
        return self._category_selections.keys()