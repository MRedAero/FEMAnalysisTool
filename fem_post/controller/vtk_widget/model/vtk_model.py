__author__ = 'Michael Redmond'

import vtk


class VTKModel(object):
    def __init__(self, view):
        super(VTKModel, self).__init__()

        self.view = view
        """:type : VTKView"""

        self.points = None
        self.grid = None
        self.color = None
        self.lookup_table = None
        self.cell_mapper = None
        self.cell_actor = None

    def set_data(self, bdf):
        """

        :param bdf: fem_reader.BDFReader
        :return:
        """

        self.points = vtk.vtkPoints()
        self.grid = vtk.vtkUnstructuredGrid()
        self.color = vtk.vtkFloatArray()
        self.lookup_table = vtk.vtkLookupTable()

        self.lookup_table.SetNumberOfTableValues(4)
        self.lookup_table.SetTableRange(0, 4)
        self.lookup_table.Build()
        self.lookup_table.SetTableValue(0, 0, 0, 0, 1) # Black
        self.lookup_table.SetTableValue(1, 1, 0, 0, 1) # Red
        self.lookup_table.SetTableValue(2, 0, 1, 0, 1) # Green
        self.lookup_table.SetTableValue(3, 0, 0, 1, 1) # Blue

        self.cell_mapper = vtk.vtkDataSetMapper()

        if self.cell_actor is not None:
            self.view.renderer.RemoveActor(self.cell_actor)

        self.cell_actor = vtk.vtkActor()

        nidMap = {}
        eidMap = {}

        grids = bdf.nodes.keys()

        for i in xrange(len(grids)):
            node = bdf.nodes[grids[i]]
            """:type : fem_reader.GRID"""
            x, y, z = node.to_global()
            tmp = self.points.InsertNextPoint(*[x, y, z])
            self.color.InsertTuple1(tmp, 0)
            nidMap[node.ID] = i

        self.grid.SetPoints(self.points)

        elements = bdf.elements.keys()

        for i in xrange(len(elements)):
            element = bdf.elements[elements[i]]
            card_name = element.card_name

            eidMap[element.ID] = i

            if card_name == 'CBEAM':
                nodes = element.nodes
                cell = vtk.vtkLine()
                ids = cell.GetPointIds()
                ids.SetId(0, nidMap[nodes[0]])
                ids.SetId(1, nidMap[nodes[1]])
                cell = self.grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
                self.color.InsertTuple1(cell, 1)
            elif card_name == 'CTRIA3':
                nodes = element.nodes
                cell = vtk.vtkTriangle()
                ids = cell.GetPointIds()
                ids.SetId(0, nidMap[nodes[0]])
                ids.SetId(1, nidMap[nodes[1]])
                ids.SetId(2, nidMap[nodes[2]])
                cell = self.grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
                self.color.InsertTuple1(cell, 2)
            elif card_name == 'CQUAD4':
                nodes = element.nodes
                cell = vtk.vtkQuad()
                ids = cell.GetPointIds()
                ids.SetId(0, nidMap[nodes[0]])
                ids.SetId(1, nidMap[nodes[1]])
                ids.SetId(2, nidMap[nodes[2]])
                ids.SetId(3, nidMap[nodes[3]])
                cell = self.grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
                self.color.InsertTuple1(cell, 3)

        self.cell_mapper.SetScalarModeToUseCellData()
        self.cell_mapper.UseLookupTableScalarRangeOn()
        self.cell_mapper.SetLookupTable(self.lookup_table)
        self.cell_mapper.SetInputData(self.grid)

        self.cell_actor.SetMapper(self.cell_mapper)
        self.cell_actor.GetProperty().EdgeVisibilityOn()

        self.view.renderer.AddActor(self.cell_actor)

        # how to get screen to update without cheating?
        self.view.interactor_style.OnLeftButtonDown()
        self.view.interactor_style.OnMouseMove()
        self.view.interactor_style.OnLeftButtonUp()