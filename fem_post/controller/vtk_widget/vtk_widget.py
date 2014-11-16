__author__ = 'Michael Redmond'

from .model import *
from .view import *
from .controller import *


class VTKWidget(object):
    def __init__(self, main_window):
        super(VTKWidget, self).__init__()

        self.view = VTKView(main_window)
        self.model = VTKModel(self.view)
        self.controller = VTKController(self.model, self.view)

    def set_background_color(self, color1=None, color2=None):
        self.controller.set_background_color(color1, color2)

    def set_data(self, bdf):
        self.model.set_data(bdf)

    @property
    def bg_color_1(self):
        return self.view.bg_color_1

    @property
    def bg_color_2(self):
        return self.view.bg_color_2