__author__ = 'Michael Redmond'

import vtk

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from fem_post.application.vtk_widget.widgets import CoordinateAxes
from fem_post.application.vtk_widget.interactor_styles import DefaultInteractorStyle


class VTKWidget(object):
    def __init__(self, window):

        self._window = window
        """:type: PyQt4.QtGui.QWidget.QWidget"""

        self._renderer = vtk.vtkRenderer()

        self._interactor = QVTKRenderWindowInteractor(self._window)

        self._interactor.GetRenderWindow().AddRenderer(self._renderer)

        # whatever self._window is, it must have a QGridLayout dynamically attached to it
        self._window.grid_layout.addWidget(self._interactor, 0, 0, 1, 1)

        self._iren = self._interactor.GetRenderWindow().GetInteractor()

        self._axes = CoordinateAxes(self._interactor)

        self._renderer.SetBackground((0, 0, 1))
        self._renderer.SetBackground2((0.8, 0.8, 1))
        self._renderer.GradientBackgroundOn()

        self._camera = vtk.vtkCamera()

        self._renderer.SetActiveCamera(self._camera)
        self._renderer.ResetCamera()

        self._interactor_style = vtk.vtkInteractorStyleRubberBandPick()
        self._interactor_style.SetDefaultRenderer(self._renderer)

        self._interactor.SetInteractorStyle(self._interactor_style)

        self._interactor.Start()

    def initialize(self):
        self._iren.Initialize()

    def unload(self):
        # this is required so that the vtk widget will release its memory
        self._window.grid_layout.removeWidget(self._interactor)
        self._interactor.Finalize()
        self._window = None