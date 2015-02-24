__author__ = 'Michael Redmond'

import vtk

from model_extract_selection_filter_base import ModelExtractSelectionFilterBase


class ModelVisibleFilter(object):
    def __init__(self):
        super(ModelVisibleFilter, self).__init__()

        self.selected = vtk.vtkIntArray()
        self.selected.SetName("visible")
        self.selected.InsertNextValue(1)
        self.selected.InsertNextValue(1)

        self.nodes = ModelExtractSelectionFilterBase(self.selected)
        self.elements = ModelExtractSelectionFilterBase(self.selected)
        self.mpcs = ModelExtractSelectionFilterBase(self.selected)

        self.input_data = None
        self.input_filter = None

        self.shown = True

    def set_input_connection(self, input_filter):

        self.input_filter = input_filter
        self.input_data = None

        self.nodes.set_input_connection(input_filter.nodes)
        self.elements.set_input_connection(input_filter.elements)
        self.mpcs.set_input_connection(input_filter.mpcs)

        self.update()

    def toggle_visible(self):
        if self.shown:
            self.shown = False
            self.selected.SetValue(0, 0)
            self.selected.SetValue(1, 0)
        else:
            self.shown = True
            self.selected.SetValue(0, 1)
            self.selected.SetValue(1, 1)

        self.update()

    def update(self):
        self.nodes.Update()
        self.elements.Update()
        self.mpcs.Update()

        self.nodes.Modified()
        self.elements.Modified()
        self.mpcs.Modified()