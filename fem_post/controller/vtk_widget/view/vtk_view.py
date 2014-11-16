__author__ = 'Michael Redmond'

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from ..widgets import *
from ..interactor_styles import *


class VTKView(object):
    def __init__(self, main_window):
        super(VTKView, self).__init__()

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

        self.interactor_style = DefaultInteractorStyle()

        self.interactor.SetInteractorStyle(self.interactor_style)

        self.interactor.Start()

        # http://www.paraview.org/Wiki/VTK/Examples/Python/Widgets/EmbedPyQt
        # http://www.vtk.org/pipermail/vtk-developers/2013-July/014005.html
        # see above why self.main_window.show() is done here

        self.main_window.show()
        self.iren.Initialize()