__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from ..vtk_globals import vtk_globals


class VisibleFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self)

        self.SetNumberOfInputPorts(1)
        self.SetNumberOfOutputPorts(1)

        self.visible = True

        self.visible_selection = vtk.vtkIntArray()
        self.visible_selection.SetName("visible")
        self.visible_selection.InsertNextValue(1)
        self.visible_selection.InsertNextValue(1)

        self.selection_vis_node = vtk.vtkSelectionNode()
        self.selection_vis_node.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)
        self.selection_vis_node.SetSelectionList(self.visible_selection)

        self.selection_vis = vtk.vtkSelection()
        self.selection_vis.AddNode(self.selection_vis_node)

        self.ex_vis = vtk.vtkExtractSelection()
        self.ex_vis.SetInputDataObject(1, self.selection_vis)

        self._callbacks = []

    def add_callback(self, callback):
        if callable(callback):
            self._callbacks.append(callback)

    def run_callbacks(self):
        for i in xrange(len(self._callbacks)):
            self._callbacks[i]()

    def FillInputPortInformation(self, port, info):
        info.Set(vtk.vtkAlgorithm.INPUT_REQUIRED_DATA_TYPE(), 'vtkUnstructuredGrid')
        return 1

    def FillOutputPortInformation(self, port, info):
        info.Set(vtk.vtkDataObject.DATA_TYPE_NAME(), 'vtkUnstructuredGrid')
        return 1

    def toggle_visible(self):
        if self.visible:
            self.visible = False
            self.visible_selection.SetValue(0, -1)
            self.visible_selection.SetValue(1, -1)
        else:
            self.visible = True
            self.visible_selection.SetValue(0, 1)
            self.visible_selection.SetValue(1, 1)

        self.selection_vis.Modified()
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):

        inp1 = vtk.vtkUnstructuredGrid.GetData(inInfo[0])

        self.ex_vis.SetInputDataObject(0, inp1)
        self.ex_vis.Modified()
        self.ex_vis.Update()

        info = outInfo.GetInformationObject(0)
        opt = vtk.vtkUnstructuredGrid.GetData(info)

        new_output = self.ex_vis.GetOutputDataObject(0)
        # to remove warnings, not used, seems to be a bug in vtk
        new_output.GetPointData().RemoveArray("vtkOriginalPointIds")

        opt.ShallowCopy(new_output)

        self.run_callbacks()

        return 1

    def all_port(self):
        return self.GetOutputPort(0)

    def all_data(self):
        return self.GetOutputDataObject(0)