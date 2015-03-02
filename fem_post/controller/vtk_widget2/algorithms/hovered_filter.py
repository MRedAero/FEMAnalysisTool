__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

#import traceback


class HoveredFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
                                        nInputPorts=1, inputType='vtkUnstructuredGrid',
                                        nOutputPorts=1, outputType='vtkPolyData')

        self.extract_edges = False
        self.edge_filter = vtk.vtkExtractEdges()
        self.edge_filter.ReleaseDataFlagOn()
        self.geom_filter = vtk.vtkGeometryFilter()
        self.geom_filter.ReleaseDataFlagOn()

    def set_extract_edges(self, value):
        self.extract_edges = value
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):

        inp = vtk.vtkUnstructuredGrid.GetData(inInfo[0])

        if inp is None or inp.GetNumberOfCells() == 0:
            return 1

        opt = vtk.vtkPolyData.GetData(outInfo.GetInformationObject(0))

        if self.extract_edges:
            self.edge_filter.SetInputData(inp)
            self.edge_filter.Modified()
            self.edge_filter.Update()
            new_output = self.edge_filter.GetOutput()
            opt.ShallowCopy(new_output)
        else:
            self.geom_filter.SetInputData(inp)
            self.geom_filter.Modified()
            self.geom_filter.Update()
            new_output = self.geom_filter.GetOutput()
            opt.ShallowCopy(new_output)

            #traceback.print_stack()

        return 1