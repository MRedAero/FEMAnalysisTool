__author__ = 'Michael Redmond'

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from .widgets import *
from .interactor_styles import *

from .model_data import *


class VTKWidget(object):
    def __init__(self, main_window):
        super(VTKWidget, self).__init__()

        self.set_up_view(main_window)

        self.data = ModelData()

        self.data_pipeline = DataPipeline(self.data, self.renderer)

        self.model_picker = ModelPicker()
        self.model_picker.set_pipeline(self.data_pipeline)
        self.model_picker.set_interactor_style(self.interactor_style)

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

        self.data.reset()

        nidMap = {}
        eidMap = {}

        grids = bdf.nodes.keys()

        self.data.node_ids.SetNumberOfTuples(len(grids))

        for i in xrange(len(grids)):
            node = bdf.nodes[grids[i]]
            """:type : fem_reader.GRID"""
            # noinspection PyArgumentList
            self.data.points.InsertNextPoint(node.to_global())
            nidMap[node.ID] = i

            cell = vtk.vtkVertex()
            ids = cell.GetPointIds()
            ids.SetId(0, i)

            self.data.nodes.InsertNextCell(cell.GetCellType(), ids)
            self.data.node_ids.SetValue(i, node.ID)
            self.data.node_visible.InsertNextValue(1)

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

                self.data.elements.InsertNextCell(cell.GetCellType(), ids)
                self.data.element_visible.InsertNextValue(1)
                self.data.element_ids.InsertNextValue(element.ID)

            elif card_name == 'CTRIA3':
                nodes = element.nodes
                cell = vtk.vtkTriangle()
                ids = cell.GetPointIds()
                ids.SetId(0, nidMap[nodes[0]])
                ids.SetId(1, nidMap[nodes[1]])
                ids.SetId(2, nidMap[nodes[2]])

                self.data.elements.InsertNextCell(cell.GetCellType(), ids)
                self.data.element_visible.InsertNextValue(1)
                self.data.element_ids.InsertNextValue(element.ID)

            elif card_name == 'CQUAD4':
                nodes = element.nodes
                cell = vtk.vtkQuad()
                ids = cell.GetPointIds()
                ids.SetId(0, nidMap[nodes[0]])
                ids.SetId(1, nidMap[nodes[1]])
                ids.SetId(2, nidMap[nodes[2]])
                ids.SetId(3, nidMap[nodes[3]])

                self.data.elements.InsertNextCell(cell.GetCellType(), ids)
                self.data.element_visible.InsertNextValue(1)
                self.data.element_ids.InsertNextValue(element.ID)

        self.data.squeeze()

        self.data_pipeline.update()

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

    def toggle_view(self):
        self.data_pipeline.toggle_shown()
        self.screen_update()

    def toggle_hidden(self):
        pass

    def screen_update(self):
        # how to get screen to update without cheating?
        self.interactor_style.OnLeftButtonDown()
        self.interactor_style.OnMouseMove()
        self.interactor_style.OnLeftButtonUp()

    def toggle_picking(self, entity_type, index=None):
        self.model_picker.toggle_picking(entity_type, index)

