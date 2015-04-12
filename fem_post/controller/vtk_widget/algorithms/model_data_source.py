__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from fem_post.controller.vtk_widget.vtk_globals import vtk_globals
from fem_post.controller.vtk_widget.model_data import ModelDataHelper2

from fem_utilities.nastran.bdf.h5 import BDFH5Reader
from fem_utilities.nastran.bdf.reader import BDFReader
from fem_utilities.nastran.bdf.utilities.bdf_card_numbering import bdf_card_numbering


class BDFDataSource(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
                                        nInputPorts=0,
                                        nOutputPorts=1, outputType='vtkUnstructuredGrid')

        self._bdf = None
        self._opt = None
        self._data = None

        self.default_group = vtk.vtkIntArray()
        self.default_group.SetName("group_default")

    def set_bdf(self, bdf):
        self._bdf = bdf
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        self._opt = vtk.vtkUnstructuredGrid.GetData(outInfo)

        self.read_bdf()

        return 1

    def read_bdf(self):

        if self._bdf is None:
            return

        bdf_reader = BDFReader(self._bdf)
        bdf_reader.read_bdf()

        h5filename = bdf_reader.h5filename

        h5_reader = BDFH5Reader(h5filename)
        ugrid = h5_reader.create_vtk_data()
        h5_reader.close()

        grid = bdf_card_numbering['GRID']
        cbeam = bdf_card_numbering['CBEAM']
        ctria3 = bdf_card_numbering['CTRIA3']
        cquad4 = bdf_card_numbering['CQUAD4']

        self._data = ModelDataHelper2(ugrid)

        data_helper = self._data

        OFFSET_NODE = vtk_globals.OFFSET_NODE
        OFFSET_ELEMENT = vtk_globals.OFFSET_ELEMENT

        self.default_group.Reset()

        VTK_NODE = vtk_globals.VTK_NODE
        VTK_VERTEX = vtk_globals.VTK_VERTEX
        VTK_LINE = vtk_globals.VTK_LINE
        VTK_TRI = vtk_globals.VTK_TRI
        VTK_QUAD = vtk_globals.VTK_QUAD
        VTK_POLY_LINE = vtk_globals.VTK_POLY_LINE

        card_ids = data_helper.card_ids
        get_card_id = card_ids.GetValue
        get_global_id = data_helper.global_ids2.GetValue
        global_id1_insert = data_helper.global_ids1.InsertNextValue
        set_global_id2 = data_helper.global_ids2.SetValue
        visible_insert = data_helper.visible.InsertNextValue
        basic_types_insert = data_helper.basic_types.InsertNextValue
        basic_shapes_insert = data_helper.basic_shapes.InsertNextValue
        default_group_insert = self.default_group.InsertNextValue

        for i in xrange(ugrid.GetNumberOfCells()):

            card_id = get_card_id(i)

            original_id = get_global_id(i)

            visible_insert(1)

            if card_id == grid:
                new_id = original_id + OFFSET_NODE
                global_id1_insert(new_id)
                set_global_id2(i, new_id)
                basic_types_insert(0)
                basic_shapes_insert(VTK_NODE)

            elif card_id == cbeam:
                new_id = original_id + OFFSET_ELEMENT
                global_id1_insert(new_id)
                set_global_id2(i, new_id)
                basic_types_insert(2)
                basic_shapes_insert(VTK_LINE)

            elif card_id == ctria3:
                new_id = original_id + OFFSET_ELEMENT
                global_id1_insert(new_id)
                set_global_id2(i, new_id)
                basic_types_insert(2)
                basic_shapes_insert(VTK_TRI)

            elif card_id == cquad4:
                new_id = original_id + OFFSET_ELEMENT
                global_id1_insert(new_id)
                set_global_id2(i, new_id)
                basic_types_insert(2)
                basic_shapes_insert(VTK_QUAD)

            else:
                # skip unsupported cell
                continue

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