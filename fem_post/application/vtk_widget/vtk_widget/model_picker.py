__author__ = 'Michael Redmond'

import vtk

from fem_post.application.vtk_widget.model_picker.single_picker import SinglePicker
from fem_post.application.vtk_widget.model_picker.box_picker import BoxPicker
from fem_post.application.vtk_widget.model_picker.poly_picker import PolyPicker


class ModelPicker(object):
    def __init__(self, vtk_widget):
        """

        :type vtk_widget: fem_post.application.vtk_widget.vtk_widget.VTKWidget
        """

        self._vtk_widget = vtk_widget

        self._single_picker = SinglePicker(self._vtk_widget)
        self._box_picker = BoxPicker(self._vtk_widget)
        self._poly_picker = PolyPicker(self._vtk_widget)

    def pick(self, pick_data):
        pick_type, pick_data = pick_data

        if pick_type == 0:
            self._single_picker.pick(pick_data)
        elif pick_type == 1:
            self._box_picker.pick(pick_data)
        elif pick_type == 2:
            self._poly_picker.pick(pick_data)