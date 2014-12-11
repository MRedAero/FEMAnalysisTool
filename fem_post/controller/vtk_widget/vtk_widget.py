__author__ = 'Michael Redmond'

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from .widgets import *
from .interactor_styles import *

from .custom_data import CustomUnstructuredGrid
from .custom_filters import ShowHideFilter


class VTKWidget(object):
    def __init__(self, main_window):
        super(VTKWidget, self).__init__()

        self.set_up_view(main_window)
        self.set_up_model()

        self.visibleFilter = ShowHideFilter()
        self.visibleFilter.widget = self

        self.show_hide = False

        self.show = True

    def set_up_view(self, main_window):
        self.main_window = main_window
        self.interactor = QVTKRenderWindowInteractor(self.main_window.ui.frame)

        self.renderer = vtk.vtkRenderer()
        self.interactor.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor.GetRenderWindow().SetAlphaBitPlanes(1)

        self.main_window.ui.vl.addWidget(self.interactor)

        self.iren = self.interactor.GetRenderWindow().GetInteractor()

        self.bg_color_1_default = (0, 0, 1)
        self.bg_color_2_default = (0.8, 0.8, 1)

        self.bg_color_1 = self.bg_color_1_default
        self.bg_color_2 = self.bg_color_2_default

        self.axes = CoordinateAxes(self.interactor)

        self.renderer.SetBackground(self.bg_color_1)
        self.renderer.SetBackground2(self.bg_color_2)
        self.renderer.GradientBackgroundOn()

        self.perspective = 0
        self.camera = vtk.vtkCamera()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()

        #self.idFilter = vtk.vtkIdFilter()

        #self.surfaceFilter = vtk.vtkDataSetSurfaceFilter()

        self.interactor_style = DefaultInteractorStyle(self)
        self.interactor_style.set_default_renderer(self.renderer)

        self.interactor.SetInteractorStyle(self.interactor_style)

        self.interactor.Start()

        # http://www.paraview.org/Wiki/VTK/Examples/Python/Widgets/EmbedPyQt
        # http://www.vtk.org/pipermail/vtk-developers/2013-July/014005.html
        # see above why self.main_window.show() is done here

        self.main_window.show()
        self.iren.Initialize()

    def set_up_model(self):
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
        self.grid = CustomUnstructuredGrid()
        self.color = vtk.vtkFloatArray()
        self.lookup_table = vtk.vtkLookupTable()

        self.lookup_table.SetNumberOfTableValues(4)
        self.lookup_table.SetTableRange(0, 4)
        self.lookup_table.Build()
        self.lookup_table.SetTableValue(0, 1, 0, 0, 0.5)  # Black
        self.lookup_table.SetTableValue(1, 1, 0, 0, 0.5)  # Red
        self.lookup_table.SetTableValue(2, 0, 0.5, 0.5, 1.)  # Green
        self.lookup_table.SetTableValue(3, 0, 0.5, 0.5, 1.)  # Green

        self.cell_mapper = vtk.vtkDataSetMapper()

        if self.cell_actor is not None:
            self.renderer.RemoveActor(self.cell_actor)

        self.cell_actor = vtk.vtkActor()

        visible = []

        nidMap = {}
        eidMap = {}

        grids = bdf.nodes.keys()

        for i in xrange(len(grids)):
            node = bdf.nodes[grids[i]]
            """:type : fem_reader.GRID"""
            # noinspection PyArgumentList
            self.points.InsertNextPoint(node.to_global())
            #self.color.InsertTuple1(tmp, 0)
            nidMap[node.ID] = i

        self.grid.data.SetPoints(self.points)

        #for i in xrange(len(grids)):
        #    cell = vtk.vtkVertex()
        #    ids = cell.GetPointIds()
        #    ids.SetId(0, i)
        #    cell = self.grid.InsertNextCell(cell.GetCellType(), ids)
        #    self.color.InsertTuple1(cell, 1)

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
                cell = self.grid.data.InsertNextCell(cell.GetCellType(), ids)  # cell.GetPointIds())
                self.color.InsertTuple1(cell, 2)
                self.grid.visible.append(1)
            elif card_name == 'CTRIA3':
                nodes = element.nodes
                cell = vtk.vtkTriangle()
                ids = cell.GetPointIds()
                ids.SetId(0, nidMap[nodes[0]])
                ids.SetId(1, nidMap[nodes[1]])
                ids.SetId(2, nidMap[nodes[2]])
                cell = self.grid.data.InsertNextCell(cell.GetCellType(), ids)  # cell.GetPointIds())
                self.color.InsertTuple1(cell, 2)
                self.grid.visible.append(1)
            elif card_name == 'CQUAD4':
                nodes = element.nodes
                cell = vtk.vtkQuad()
                ids = cell.GetPointIds()
                ids.SetId(0, nidMap[nodes[0]])
                ids.SetId(1, nidMap[nodes[1]])
                ids.SetId(2, nidMap[nodes[2]])
                ids.SetId(3, nidMap[nodes[3]])
                cell = self.grid.data.InsertNextCell(cell.GetCellType(), ids)  # cell.GetPointIds())
                self.color.InsertTuple1(cell, 3)
                self.grid.visible.append(1)

        self.grid.data.GetCellData().SetScalars(self.color)

        self.visibleFilter.SetInputData(self.grid.data)

        self.visibleFilter.input = self.grid
        self.visibleFilter.Update()
        #self.visibleFilter.execute()

        #self.cell_mapper.SetScalarModeToUseCellData()
        #self.cell_mapper.UseLookupTableScalarRangeOn()
        #self.cell_mapper.SetLookupTable(self.lookup_table)
        self.cell_mapper.SetInputData(self.data)

        #self.cell_mapper.SetInputData(self.visibleFilter.output)

        self.cell_actor.SetMapper(self.cell_mapper)
        self.cell_actor.GetProperty().EdgeVisibilityOn()
        #self.cell_actor.GetProperty().SetColor(0, 1, 0)


        #self.cell_actor.GetProperty().SetPointSize(6)
        #self.cell_actor.GetProperty().SetOpacity(0.95)

        self.renderer.AddActor(self.cell_actor)

        self.interactor_style.cell_picker.SetDataSet(self.data)
        self.interactor_style.cell_data_set = True

        self.interactor_style.point_picker.add_pick_list(self.cell_actor)
        self.interactor_style.point_data_set = True

        self.screen_update()

    def set_background_color(self, color1=None, color2=None):
        if color1 is not None:
            self.bg_color_1 = color1
            self.renderer.SetBackground(color1)

        if color2 is not None:
            self.bg_color_2 = color2
            self.renderer.SetBackground2(color2)

    def toggle_perspective(self):
        if self.perspective == 0:
            self.camera.ParallelProjectionOn()
            self.perspective = 1
        else:
            self.camera.ParallelProjectionOff()
            self.perspective = 0

    def show_hide_check(self):
        if self.show_hide:
            self.show_hide = False
        else:
            self.show_hide = True

    def show_hide_button_clicked(self):

        if self.show:
            self.show = False
        else:
            self.show = True

        self.visibleFilter.execute()

        if self.cell_mapper is None:
            return

        self.cell_mapper.SetInputData(self.data)
        self.cell_mapper.Modified()
        self.screen_update()

        self.interactor_style.cell_picker.SetDataSet(self.data)

    @property
    def data(self):
        if self.show:
            return self.visibleFilter.shown.data
        else:
            return self.visibleFilter.hidden.data

    @property
    def custom_data(self):
        if self.show:
            return self.visibleFilter.shown
        else:
            return self.visibleFilter.hidden

    def cell_id(self, id):
        if self.show:
            return self.visibleFilter.shown.map[id]
        else:
            return self.visibleFilter.hidden.map[id]

    def screen_update(self):
        # how to get screen to update without cheating?
        self.interactor_style.OnLeftButtonDown()
        self.interactor_style.OnMouseMove()
        self.interactor_style.OnLeftButtonUp()