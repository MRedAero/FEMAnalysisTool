__author__ = 'Michael Redmond'

import vtk


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

        self.data_order = ['Node', 'Element', 'MPC', 'Load', 'Disp']

        self.RANGE_NODE = [0, 99999999]
        self.RANGE_ELEMENT = [self.RANGE_NODE[1] + 1, self.RANGE_NODE[1] + 100000000]
        self.RANGE_MPC = [self.RANGE_ELEMENT[1] + 1, self.RANGE_ELEMENT[1] + 100000000]
        self.RANGE_LOAD = [self.RANGE_MPC[1] + 1, self.RANGE_MPC[1] + 100000000]

        self.OFFSET_NODE = self.RANGE_NODE[0]
        self.OFFSET_ELEMENT = self.RANGE_ELEMENT[0]
        self.OFFSET_MPC = self.RANGE_MPC[0]
        self.OFFSET_LOAD = self.RANGE_LOAD[0]

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

        self.TYPE_NODE = vtk.vtkIntArray()
        self.TYPE_NODE.SetName("basic_types")
        self.TYPE_NODE.SetNumberOfTuples(2)
        self.TYPE_NODE.SetNumberOfComponents(1)
        self.TYPE_NODE.SetValue(0, 0)
        self.TYPE_NODE.SetValue(1, self.data_order.index('Node'))

        self.TYPE_VERTEX = vtk.vtkIntArray()
        self.TYPE_VERTEX.SetName("basic_types")
        self.TYPE_VERTEX.SetNumberOfTuples(2)
        self.TYPE_VERTEX.SetNumberOfComponents(1)
        self.TYPE_VERTEX.SetValue(0, 1)
        self.TYPE_VERTEX.SetValue(1, 1)

        self.TYPE_ELEMENT = vtk.vtkIntArray()
        self.TYPE_ELEMENT.SetName("basic_types")
        self.TYPE_ELEMENT.SetNumberOfTuples(2)
        self.TYPE_ELEMENT.SetNumberOfComponents(1)
        self.TYPE_ELEMENT.SetValue(0, 2)
        self.TYPE_ELEMENT.SetValue(1, 2)

        self.TYPE_MPC = vtk.vtkIntArray()
        self.TYPE_MPC.SetName("basic_types")
        self.TYPE_MPC.SetNumberOfTuples(2)
        self.TYPE_MPC.SetNumberOfComponents(1)
        self.TYPE_MPC.SetValue(0, 3)
        self.TYPE_MPC.SetValue(1, 3)

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