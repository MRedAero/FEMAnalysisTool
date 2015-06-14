__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from fem_post.application.vtk_widget.vtk_globals import vtk_globals


class SplitDataFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
                                        nInputPorts=1, inputType='vtkUnstructuredGrid',
                                        nOutputPorts=7, outputType='vtkUnstructuredGrid')

        self.selection_node = vtk.vtkSelectionNode()
        self.selection = vtk.vtkSelection()
        self.ex = vtk.vtkExtractSelection()
        self.ex.ReleaseDataFlagOn()

        self.selection_node.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)
        self.selection.AddNode(self.selection_node)
        self.ex.SetInputDataObject(1, self.selection)

    def RequestData(self, request, inInfo, outInfo):

        inp = vtk.vtkUnstructuredGrid.GetData(inInfo[0])

        if inp is None or inp.GetNumberOfCells() == 0:
            return 1

        self.ex.SetInputDataObject(0, inp)

        # nodes
        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(0))
        self.selection_node.SetSelectionList(vtk_globals.CATEGORY_SELECTION['node'])
        self.selection_node.Modified()
        self.selection.Modified()
        self.ex.Modified()
        self.ex.Update()
        new_output = self.ex.GetOutput()
        opt.ShallowCopy(new_output)

        # vertices
        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(1))
        self.selection_node.SetSelectionList(vtk_globals.CATEGORY_SELECTION['vertex'])
        self.selection_node.Modified()
        self.selection.Modified()
        self.ex.Modified()
        self.ex.Update()
        new_output = self.ex.GetOutput()
        opt.ShallowCopy(new_output)

        # elements
        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(2))
        self.selection_node.SetSelectionList(vtk_globals.CATEGORY_SELECTION['element'])
        self.selection_node.Modified()
        self.selection.Modified()
        self.ex.Modified()
        self.ex.Update()
        new_output = self.ex.GetOutput()
        opt.ShallowCopy(new_output)

        # mpcs
        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(3))
        self.selection_node.SetSelectionList(vtk_globals.CATEGORY_SELECTION['mpc'])
        self.selection_node.Modified()
        self.selection.Modified()
        self.ex.Modified()
        self.ex.Update()
        new_output = self.ex.GetOutput()
        opt.ShallowCopy(new_output)

        # force
        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(4))
        self.selection_node.SetSelectionList(vtk_globals.CATEGORY_SELECTION['force'])
        self.selection_node.Modified()
        self.selection.Modified()
        self.ex.Modified()
        self.ex.Update()
        new_output = self.ex.GetOutput()
        opt.ShallowCopy(new_output)

        # disp
        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(5))
        self.selection_node.SetSelectionList(vtk_globals.CATEGORY_SELECTION['disp'])
        self.selection_node.Modified()
        self.selection.Modified()
        self.ex.Modified()
        self.ex.Update()
        new_output = self.ex.GetOutput()
        opt.ShallowCopy(new_output)

        # coords
        opt = vtk.vtkUnstructuredGrid.GetData(outInfo.GetInformationObject(6))
        self.selection_node.SetSelectionList(vtk_globals.CATEGORY_SELECTION['coord'])
        self.selection_node.Modified()
        self.selection.Modified()
        self.ex.Modified()
        self.ex.Update()
        new_output = self.ex.GetOutput()
        opt.ShallowCopy(new_output)

        return 1

    def node_port(self):
        return self.GetOutputPort(0)

    def vertex_port(self):
        return self.GetOutputPort(1)

    def element_port(self):
        return self.GetOutputPort(2)

    def mpc_port(self):
        return self.GetOutputPort(3)

    def force_port(self):
        return self.GetOutputPort(4)

    def disp_port(self):
        return self.GetOutputPort(5)

    def coord_port(self):
        return self.GetOutputPort(6)

    def node_data(self):
        return self.GetOutputDataObject(0)

    def vertex_data(self):
        return self.GetOutputDataObject(1)

    def element_data(self):
        return self.GetOutputDataObject(2)

    def mpc_data(self):
        return self.GetOutputDataObject(3)

    def force_data(self):
        return self.GetOutputDataObject(4)

    def disp_data(self):
        return self.GetOutputDataObject(5)

    def coord_data(self):
        return self.GetOutputDataObject(6)