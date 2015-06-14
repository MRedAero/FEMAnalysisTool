__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from fem_post.application.vtk_widget.vtk_globals import vtk_globals
from fem_post.application.vtk_widget.model_data import ModelDataHelper2
from fem_utilities.nastran.bdf.utilities.bdf_card_numbering import bdf_card_code


class BDFDataSource(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
                                        nInputPorts=0,
                                        nOutputPorts=1, outputType='vtkUnstructuredGrid')

        self._file = None
        self._opt = None
        self._data = None

        self.default_group = vtk.vtkIntArray()
        self.default_group.SetName("group_default")

    def set_file(self, file):
        self._file = file
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        self._opt = vtk.vtkUnstructuredGrid.GetData(outInfo)

        self.read_bdf()

        return 1

    def read_bdf(self):

        if self._file is None:
            return

        h5_reader = self._file

        ugrid = h5_reader.create_vtk_data()
        h5_reader.close()

        self._data = ModelDataHelper2(ugrid)

        data_helper = self._data

        offsets = vtk_globals.offsets

        self.default_group.Reset()

        get_global_id = data_helper.global_ids2.GetValue
        global_id1_insert = data_helper.global_ids1.InsertNextValue
        set_global_id2 = data_helper.global_ids2.SetValue
        visible_insert = data_helper.visible.InsertNextValue
        default_group_insert = self.default_group.InsertNextValue
        basic_types_get = data_helper.basic_types.GetValue

        for i in xrange(ugrid.GetNumberOfCells()):

            original_id = get_global_id(i)

            visible_insert(1)

            card_type = basic_types_get(i)

            offset = offsets[card_type]

            new_id = original_id + offset
            global_id1_insert(new_id)
            set_global_id2(i, new_id)

            default_group_insert(new_id)

        data_helper.squeeze()

        self.default_group.Squeeze()
        self.default_group.Modified()

        self._opt.ShallowCopy(ugrid)

        self._bdf = None


if __name__ == '__main__':
    data = BDFDataSource()

    data.set_bdf(r'D:\nastran\wing.bdf')

    data.Update()

    print data.GetOutputDataObject(0)

    while True:
        pass