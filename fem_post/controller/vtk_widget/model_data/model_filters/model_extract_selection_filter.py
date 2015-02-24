__author__ = 'Michael Redmond'

import vtk

from model_extract_selection_filter_base import ModelExtractSelectionFilterBase


class ModelExtractSelectionFilter(object):
    def __init__(self):
        super(ModelExtractSelectionFilter, self).__init__()

        self.nodes = ModelExtractSelectionFilterBase()
        self.elements = ModelExtractSelectionFilterBase()
        self.mpcs = ModelExtractSelectionFilterBase()

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

    def set_input_data(self, input_data):

        self.input_filter = None
        self.input_data = input_data

        self.nodes.set_input_data(input_data.nodes)
        self.elements.set_input_data(input_data.elements)
        self.mpcs.set_input_data(input_data.mpcs)

        self.update()

    def set_selection_list(self, selection):
        self.nodes.set_selection_list(selection['nodes'])
        self.elements.set_selection_list(selection['elements'])
        self.mpcs.set_input_data(selection['mpcs'])

    def select_integers(self):
        self.nodes.select_integers()
        self.elements.select_integers()
        self.mpcs.select_integers()

    def select_floats(self):
        self.nodes.select_floats()
        self.elements.select_floats()
        self.mpcs.select_floats()

    def filter_thresholds(self):
        self.nodes.filter_thresholds()
        self.elements.filter_thresholds()
        self.mpcs.filter_thresholds()

    def filter_ids(self):
        self.nodes.filter_ids()
        self.elements.filter_ids()
        self.mpcs.filter_ids()

    def filter_global_ids(self):
        self.nodes.filter_global_ids()
        self.elements.filter_global_ids()
        self.mpcs.filter_global_ids()

    def update(self):
        self.nodes.Update()
        self.elements.Update()
        self.mpcs.Update()

        self.nodes.Modified()
        self.elements.Modified()
        self.mpcs.Modified()