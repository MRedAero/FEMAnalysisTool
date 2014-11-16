__author__ = 'Michael Redmond'

from .view import *


class VTKWidget(object):
    def __init__(self, main_window):
        super(VTKWidget, self).__init__()

        # self.model = VTKModel()
        self.view = VTKView(main_window)
        # self.controller = VTKController()

    def set_background_color(self, color1=None, color2=None):
        self.view.set_background_color(color1, color2)

    @property
    def bg_color_1(self):
        return self.view.bg_color_1

    @property
    def bg_color_2(self):
        return self.view.bg_color_2