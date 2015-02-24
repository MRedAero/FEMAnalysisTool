__author__ = 'Michael Redmond'

import vtk

from ..model_mappers import ModelMapper2D
from ..model_actors import ModelActor2D


class DataPipeline2D(object):
    def __init__(self, model_data_filter, renderer):
        super(DataPipeline2D, self).__init__()

        self.model_data_filter = model_data_filter
        self.renderer = renderer

        self.mapper = ModelMapper2D(model_data_filter)
        #self.mapper.set_input_connection(self.model_data_filter)

        self.actor = ModelActor2D()
        self.actor.set_mapper(self.mapper)
        self.set_renderer(self.renderer)

        self.update()

    def set_data(self, model_data):
        self.model_data = model_data
        self.group_filter.set_input_data(self.model_data)
        self.update()

    def get_data(self):
        return self.model_data

    def set_renderer(self, renderer):
        self.actor.remove_renderer()

        self.renderer = renderer
        self.actor.set_renderer(self.renderer)
        self.update()

    def get_renderer(self):
        return self.renderer

    def update(self):
        self.model_data.update()
        self.mapper.update()