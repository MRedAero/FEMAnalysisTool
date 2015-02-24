__author__ = 'Michael Redmond'

import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from ..vtk_globals import vtk_globals
from ..model_data import ModelDataHelper

from fem_reader import BDFReader


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

        new_data = vtk.vtkUnstructuredGrid()

        self._data = ModelDataHelper(new_data)

        data_helper = self._data

        bdf = self._bdf

        if bdf is None:
            return

        nid_map = {}
        eid_map = {}

        grids = bdf.nodes.keys()

        OFFSET_NODE = vtk_globals.OFFSET_NODE
        OFFSET_ELEMENT = vtk_globals.OFFSET_ELEMENT

        self.default_group.Reset()

        original_id = 0

        VTK_NODE = vtk_globals.VTK_NODE
        VTK_VERTEX = vtk_globals.VTK_VERTEX
        VTK_LINE = vtk_globals.VTK_LINE
        VTK_TRI = vtk_globals.VTK_TRI
        VTK_QUAD = vtk_globals.VTK_QUAD
        VTK_POLY_LINE = vtk_globals.VTK_POLY_LINE

        for i in xrange(len(grids)):
            node = bdf.nodes[grids[i]]
            """:type : fem_reader.GRID"""
            # noinspection PyArgumentList
            data_helper.points.InsertNextPoint(node.to_global())
            nid_map[node.ID] = i

            cell = vtk.vtkVertex()
            ids = cell.GetPointIds()
            ids.SetId(0, i)

            data_helper.data.InsertNextCell(cell.GetCellType(), ids)
            data_helper.global_ids1.InsertNextValue(node.ID + OFFSET_NODE)
            data_helper.global_ids2.InsertNextValue(node.ID + OFFSET_NODE)
            data_helper.visible.InsertNextValue(1)
            data_helper.basic_types.InsertNextValue(0)
            data_helper.basic_shapes.InsertNextValue(VTK_NODE)
            data_helper.original_ids.InsertNextValue(original_id)
            original_id += 1

            # add to default group
            self.default_group.InsertNextValue(node.ID + OFFSET_NODE)

        elements = bdf.elements.keys()

        for i in xrange(len(elements)):
            element = bdf.elements[elements[i]]
            card_name = element.card_name

            eid_map[element.ID] = i

            number_of_nodes = len(element.nodes)

            if number_of_nodes == 1:
                #  some 1 node elements, add to data.vertices.data
                #data.elements.basic_types.InsertNextValue(1)
                pass

            elif card_name == 'CBEAM':
                nodes = element.nodes
                cell = vtk.vtkLine()
                ids = cell.GetPointIds()
                ids.SetId(0, nid_map[nodes[0]])
                ids.SetId(1, nid_map[nodes[1]])

                data_helper.data.InsertNextCell(cell.GetCellType(), ids)
                data_helper.visible.InsertNextValue(1)
                data_helper.global_ids1.InsertNextValue(element.ID + OFFSET_ELEMENT)
                data_helper.global_ids2.InsertNextValue(element.ID + OFFSET_ELEMENT)
                data_helper.original_ids.InsertNextValue(original_id)
                original_id += 1

                # add to default group
                self.default_group.InsertNextValue(element.ID + OFFSET_ELEMENT)

                data_helper.basic_types.InsertNextValue(2)
                data_helper.basic_shapes.InsertNextValue(VTK_LINE)

            elif card_name == 'CTRIA3':
                nodes = element.nodes
                cell = vtk.vtkTriangle()
                ids = cell.GetPointIds()
                ids.SetId(0, nid_map[nodes[0]])
                ids.SetId(1, nid_map[nodes[1]])
                ids.SetId(2, nid_map[nodes[2]])

                data_helper.data.InsertNextCell(cell.GetCellType(), ids)
                data_helper.visible.InsertNextValue(1)
                data_helper.global_ids1.InsertNextValue(element.ID + OFFSET_ELEMENT)
                data_helper.global_ids2.InsertNextValue(element.ID + OFFSET_ELEMENT)
                data_helper.original_ids.InsertNextValue(original_id)
                original_id += 1

                # add to default group
                self.default_group.InsertNextValue(element.ID + OFFSET_ELEMENT)

                data_helper.basic_types.InsertNextValue(2)
                data_helper.basic_shapes.InsertNextValue(VTK_TRI)

            elif card_name == 'CQUAD4':
                nodes = element.nodes
                cell = vtk.vtkQuad()
                ids = cell.GetPointIds()
                ids.SetId(0, nid_map[nodes[0]])
                ids.SetId(1, nid_map[nodes[1]])
                ids.SetId(2, nid_map[nodes[2]])
                ids.SetId(3, nid_map[nodes[3]])

                data_helper.data.InsertNextCell(cell.GetCellType(), ids)
                data_helper.visible.InsertNextValue(1)
                data_helper.global_ids1.InsertNextValue(element.ID + OFFSET_ELEMENT)
                data_helper.global_ids2.InsertNextValue(element.ID + OFFSET_ELEMENT)
                data_helper.original_ids.InsertNextValue(original_id)
                original_id += 1

                # add to default group
                self.default_group.InsertNextValue(element.ID + OFFSET_ELEMENT)

                data_helper.basic_types.InsertNextValue(2)
                data_helper.basic_shapes.InsertNextValue(VTK_QUAD)

        data_helper.squeeze()

        self.default_group.Squeeze()
        self.default_group.Modified()

        self._opt.ShallowCopy(new_data)


if __name__ == '__main__':
    data = BDFDataSource()

    data.set_bdf(r'D:\nastran\wing.bdf')

    data.Update()

    print data.GetOutputDataObject(0)

    while True:
        pass