__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from controller.vtk_widget.vtk_globals import vtk_globals


class GroupFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self)

        self.SetNumberOfInputPorts(1)
        self.SetNumberOfOutputPorts(1)

        self.selection_group = vtk.vtkSelection()

        self.ex_group = vtk.vtkExtractSelection()
        self.ex_group.ReleaseDataFlagOn()
        self.ex_group.SetInputDataObject(1, self.selection_group)

    def set_group_selections(self, selections):
        self.group_selections = selections
        self.Modified()

    def FillInputPortInformation(self, port, info):
        info.Set(vtk.vtkAlgorithm.INPUT_REQUIRED_DATA_TYPE(), 'vtkUnstructuredGrid')
        return 1

    def FillOutputPortInformation(self, port, info):
        info.Set(vtk.vtkDataObject.DATA_TYPE_NAME(), 'vtkUnstructuredGrid')
        return 1

    def RequestData(self, request, inInfo, outInfo):

        inp1 = vtk.vtkUnstructuredGrid.GetData(inInfo[0])

        self.selection_group.RemoveAllNodes()

        group_selections = self.group_selections

        if group_selections is not None:

            for i in xrange(group_selections.GetNumberOfArrays()):
                node = vtk.vtkSelectionNode()
                node.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)
                node.SetSelectionList(group_selections.GetArray(i))

                self.selection_group.AddNode(node)

        self.selection_group.Modified()

        self.ex_group.SetInputDataObject(0, inp1)

        self.ex_group.Update()

        info = outInfo.GetInformationObject(0)
        opt = vtk.vtkUnstructuredGrid.GetData(info)

        new_output = self.ex_group.GetOutputDataObject(0)
        # to remove warnings, not used, seems to be a bug in vtk
        new_output.GetPointData().RemoveArray("vtkOriginalPointIds")

        opt.ShallowCopy(new_output)

        return 1