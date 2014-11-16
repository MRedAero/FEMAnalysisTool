__author__ = 'Michael Redmond'

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from .coordinate_axes import CoordinateAxes
from .interactor_style import *


class VTKController(object):
    def __init__(self, main_window):
        super(VTKController, self).__init__()

        self.main_window = main_window
        self.interactor = QVTKRenderWindowInteractor(self.main_window.ui.frame)

        self.ren = vtk.vtkRenderer()
        self.interactor.GetRenderWindow().AddRenderer(self.ren)
        self.interactor.GetRenderWindow().SetAlphaBitPlanes(1)

        self.main_window.ui.vl.addWidget(self.interactor)

        self.iren = self.interactor.GetRenderWindow().GetInteractor()

        self.bgcolor1_default = (0, 0, 1)
        self.bgcolor2_default = (0.8, 0.8, 1)

        self.bgcolor1 = self.bgcolor1_default
        self.bgcolor2 = self.bgcolor2_default

        self.axes = CoordinateAxes(self.interactor)

        self.ren.SetBackground(self.bgcolor1)
        self.ren.SetBackground2(self.bgcolor2)
        self.ren.GradientBackgroundOn()

        self.interactor_style = DefaultInteractorStyle()

        self.interactor.SetInteractorStyle(self.interactor_style)

        self.interactor.Start()
        self.iren.Initialize()

    def set_background_color(self, color1=None, color2=None):
        if color1 is not None:
            self.bgcolor1 = color1
            self.ren.SetBackground(color1)

        if color2 is not None:
            self.bgcolor2 = color2
            self.ren.SetBackground2(color2)

        