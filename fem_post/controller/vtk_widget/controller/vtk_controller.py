__author__ = 'Michael Redmond'

import vtk


class VTKController(object):
    def __init__(self, model, view):
        super(VTKController, self).__init__()
        self.model = model
        self.view = view

    def set_background_color(self, color1=None, color2=None):
        if color1 is not None:
            self.view.bg_color_1 = color1
            self.view.renderer.SetBackground(color1)

        if color2 is not None:
            self.view.bg_color_2 = color2
            self.view.renderer.SetBackground2(color2)