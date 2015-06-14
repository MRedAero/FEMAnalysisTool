__author__ = 'Michael Redmond'

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import vtk_pub


class VTKView(object):
    """
    Contains renderers, interactor, camera
    """
    def __init__(self, vtk_widget):
        """

        :type vtk_widget: fem_post.application.vtk_widget.VTKWidget
        :return:
        """
        self._vtk_widget = vtk_widget

        self._renderer = vtk.vtkRenderer() #  self._vtk_widget.renderer
        self._renderer_picked = vtk.vtkRenderer() #  self._vtk_widget.renderer_picked
        self._renderer_hovered = vtk.vtkRenderer() #  self._vtk_widget.renderer_hovered

        self._interactor = QVTKRenderWindowInteractor(self._vtk_widget.get_main_window())

        self._renderer.SetLayer(0)
        self._renderer.SetInteractive(1)

        self._renderer_picked.SetLayer(1)
        self._renderer_picked.SetInteractive(1)

        self._renderer_hovered.SetLayer(2)
        self._renderer_hovered.SetInteractive(1)

        render_window = self._interactor.GetRenderWindow()
        render_window.SetNumberOfLayers(3)
        render_window.AddRenderer(self._renderer_hovered)
        render_window.AddRenderer(self._renderer_picked)
        render_window.AddRenderer(self._renderer)
        render_window.SetAlphaBitPlanes(1)

        self._bg_color_1_default = (0, 0, 1)
        self._bg_color_2_default = (0.8, 0.8, 1)

        self._bg_color_1 = self._bg_color_1_default
        self._bg_color_2 = self._bg_color_2_default

        self._renderer.SetBackground(self._bg_color_1)
        self._renderer.SetBackground2(self._bg_color_2)
        self._renderer.GradientBackgroundOn()

        self._perspective = 0
        self._camera = vtk.vtkCamera()

        self._renderer.SetActiveCamera(self._camera)
        self._renderer.ResetCamera()

        self._renderer_picked.SetActiveCamera(self._camera)
        self._renderer_hovered.SetActiveCamera(self._camera)

        self._subscribe_to_pub()

    def _subscribe_to_pub(self):
        pub = self._vtk_widget.get_pub()
        pub.subscribe(self.fit_view, vtk_pub.subscribe.fit_view())

    def get_renderers(self):
        return self._renderer, self._renderer_picked, self._renderer_hovered

    def get_interactor(self):
        return self._interactor

    def fit_view(self):
        self._renderer.ResetCamera()
        self.render()

    def render(self):
        self._interactor.GetRenderWindow().Render()