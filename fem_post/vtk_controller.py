__author__ = 'Michael Redmond'

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VTKController(object):
    def __init__(self, ui):
        self.ui = ui
        self.interactor = QVTKRenderWindowInteractor(self.ui.frame)

        self.ren = vtk.vtkRenderer()
        self.interactor.GetRenderWindow().AddRenderer(self.ren)
        self.interactor.GetRenderWindow().SetAlphaBitPlanes(1)

        self.ui.vl.addWidget(self.interactor)

        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren = self.interactor.GetRenderWindow().GetInteractor()

        self.bgcolor1 = (0, 0, 1)
        self.bgcolor2 = (0.8, 0.8, 1)

        self.ren.SetBackground(self.bgcolor1)
        self.ren.SetBackground2(self.bgcolor2)
        self.ren.GradientBackgroundOn()

        self.interactor.Start()
        self.iren.Initialize()

    def set_background_color(self, color1=None, color2=None):
        if color1 is not None:
            self.bgcolor1 = color1
            self.ren.SetBackground(color1)

        if color2 is not None:
            self.bgcolor2 = color2
            self.ren.SetBackground2(color2)

        