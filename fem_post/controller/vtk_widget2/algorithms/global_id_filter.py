__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase


class GlobalIdFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
                                        nInputPorts=1, inputType='vtkUnstructuredGrid',
                                        nOutputPorts=1, outputType='vtkUnstructuredGrid')

        self.selection_list = vtk.vtkIntArray()

        self.selection_node = vtk.vtkSelectionNode()
        self.selection_node.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)
        self.selection_node.SetSelectionList(self.selection_list)

        self.selection = vtk.vtkSelection()
        self.selection.AddNode(self.selection_node)

        self.ex = vtk.vtkExtractSelection()
        self.ex.SetInputDataObject(1, self.selection)

    def set_selection_list(self, selection_list):
        self.selection_list.Reset()

        if hasattr(selection_list, 'all_selection'):
            selection_list = selection_list.all_selection()

        self.selection_list.SetNumberOfTuples(len(selection_list))

        my_int = int

        for i in xrange(len(selection_list)):
            self.selection_list.SetValue(i, my_int(selection_list[i]))

        self.Modified()
        self.Update()

    def RequestData(self, request, inInfo, outInfo):

        inp = vtk.vtkUnstructuredGrid.GetData(inInfo[0])

        if inp is None or inp.GetNumberOfCells() == 0:
            return 1

        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(0))

        self.ex.SetInputDataObject(0, inp)
        self.ex.Modified()
        self.ex.Update()

        new_output = self.ex.GetOutputDataObject(0)

        opt.ShallowCopy(new_output)

        return 1