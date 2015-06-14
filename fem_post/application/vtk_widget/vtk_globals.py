__author__ = 'Michael Redmond'

import vtk

from fem_utilities.nastran.bdf.utilities.bdf_card_numbering import card_category


class VTKGlobals(object):
    def __init__(self):
        super(VTKGlobals, self).__init__()

        self.VTK_VERSION = vtk.vtkVersion().GetVTKMajorVersion()

        self.VTK_NODE = 0
        self.VTK_VERTEX = 1
        self.VTK_LINE = 3
        self.VTK_POLY_LINE = 4
        self.VTK_TRI = 5
        self.VTK_QUAD = 9

        self.SELECTION_REPLACE = 0
        self.SELECTION_APPEND = 1
        self.SELECTION_REMOVE = 2

        self.SELECTION_SINGLE = 0
        self.SELECTION_BOX = 1
        self.SELECTION_POLY = 2

        self.data_order = ['Node', 'Element', 'MPC', 'Load', 'Disp', 'Coord']

        self.RANGE_NODE = [0, 99999999]
        self.RANGE_ELEMENT = [self.RANGE_NODE[1] + 1, self.RANGE_NODE[1] + 100000000]
        self.RANGE_MPC = [self.RANGE_ELEMENT[1] + 1, self.RANGE_ELEMENT[1] + 100000000]
        self.RANGE_LOAD = [self.RANGE_MPC[1] + 1, self.RANGE_MPC[1] + 100000000]
        self.RANGE_DISP = [self.RANGE_LOAD[1] + 1, self.RANGE_LOAD[1] + 100000000]
        self.RANGE_COORD = [self.RANGE_DISP[1] + 1, self.RANGE_DISP[1] + 100000000]

        self.OFFSET_NODE = self.RANGE_NODE[0]
        self.OFFSET_ELEMENT = self.RANGE_ELEMENT[0]
        self.OFFSET_MPC = self.RANGE_MPC[0]
        self.OFFSET_LOAD = self.RANGE_LOAD[0]
        self.OFFSET_DISP = self.RANGE_DISP[0]
        self.OFFSET_COORD = self.RANGE_COORD[0]

        self.offsets = [self.OFFSET_NODE, self.OFFSET_ELEMENT, self.OFFSET_ELEMENT,
                        self.OFFSET_MPC, self.OFFSET_LOAD, self.OFFSET_DISP, self.OFFSET_COORD]

        self.THRESHOLD_NODE = vtk.vtkIntArray()
        self.THRESHOLD_NODE.SetName("global_ids")
        self.THRESHOLD_NODE.SetNumberOfTuples(2)
        self.THRESHOLD_NODE.SetNumberOfComponents(1)
        self.THRESHOLD_NODE.SetValue(0, self.RANGE_NODE[0])
        self.THRESHOLD_NODE.SetValue(1, self.RANGE_NODE[1])

        self.THRESHOLD_ELEMENT = vtk.vtkIntArray()
        self.THRESHOLD_ELEMENT.SetName("global_ids")
        self.THRESHOLD_ELEMENT.SetNumberOfTuples(2)
        self.THRESHOLD_ELEMENT.SetNumberOfComponents(1)
        self.THRESHOLD_ELEMENT.SetValue(0, self.RANGE_ELEMENT[0])
        self.THRESHOLD_ELEMENT.SetValue(1, self.RANGE_ELEMENT[1])

        self.THRESHOLD_MPC = vtk.vtkIntArray()
        self.THRESHOLD_MPC.SetName("global_ids")
        self.THRESHOLD_MPC.SetNumberOfTuples(2)
        self.THRESHOLD_MPC.SetNumberOfComponents(1)
        self.THRESHOLD_MPC.SetValue(0, self.RANGE_MPC[0])
        self.THRESHOLD_MPC.SetValue(1, self.RANGE_MPC[1])

        self.THRESHOLD_FORCE = vtk.vtkIntArray()
        self.THRESHOLD_FORCE.SetName("global_ids")
        self.THRESHOLD_FORCE.SetNumberOfTuples(2)
        self.THRESHOLD_FORCE.SetNumberOfComponents(1)
        self.THRESHOLD_FORCE.SetValue(0, self.RANGE_LOAD[0])
        self.THRESHOLD_FORCE.SetValue(1, self.RANGE_LOAD[1])

        self.THRESHOLD_DISP = vtk.vtkIntArray()
        self.THRESHOLD_DISP.SetName("global_ids")
        self.THRESHOLD_DISP.SetNumberOfTuples(2)
        self.THRESHOLD_DISP.SetNumberOfComponents(1)
        self.THRESHOLD_DISP.SetValue(0, self.RANGE_DISP[0])
        self.THRESHOLD_DISP.SetValue(1, self.RANGE_DISP[1])

        self.THRESHOLD_COORD = vtk.vtkIntArray()
        self.THRESHOLD_COORD.SetName("global_ids")
        self.THRESHOLD_COORD.SetNumberOfTuples(2)
        self.THRESHOLD_COORD.SetNumberOfComponents(1)
        self.THRESHOLD_COORD.SetValue(0, self.RANGE_COORD[0])
        self.THRESHOLD_COORD.SetValue(1, self.RANGE_COORD[1])

        self.CATEGORY_SELECTION = {}
        categories = ['node', 'vertex', 'element', 'mpc', 'force', 'disp', 'coord']

        for category in categories:
            selection_type = vtk.vtkIntArray()
            self.CATEGORY_SELECTION[category] = selection_type

            selection_type.SetName("basic_types")
            selection_type.SetNumberOfTuples(2)
            selection_type.SetNumberOfComponents(1)
            selection_type.SetValue(0, card_category[category])
            selection_type.SetValue(1, card_category[category])


    def global_id(self, eid):
        eid = int(eid)
        a = 100000000
        return eid - a*int(eid/a)

    def cell_type(self, eid):
        eid = int(eid)
        return self.data_order[int(eid/100000000)]


vtk_globals = VTKGlobals()


if __name__ == '__main__':
    id = 99999999
    print int(id/100000000)

    id = 199999999
    print int(id/100000000)

    id = 599999999
    print int(id/100000000)