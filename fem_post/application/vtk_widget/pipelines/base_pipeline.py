__author__ = 'Michael Redmond'

from collections import OrderedDict

import vtk

from fem_post.application.vtk_widget.algorithms import AbstractSplitDataFilter


class BasePipeline(object):
    def __init__(self, renderer, input_filter):
        super(BasePipeline, self).__init__()

        self._input_filter = None

        self._categories = []

        self._mappers = OrderedDict()
        self._actors = OrderedDict()

        self._renderer = None

        if input_filter is not None:
            self.set_input_filter(input_filter)

        if renderer is not None:
            self.set_renderer(renderer)

    def set_input_filter(self, input_filter):

        if self._input_filter is not None:
            e = Exception("input_filter is already set!")
            raise e

        assert issubclass(input_filter.__class__, AbstractSplitDataFilter)

        self._input_filter = input_filter

        self._categories = self._input_filter.get_categories()

        self._mappers = OrderedDict()
        self._actors = OrderedDict()

        for category in self._categories:
            mapper = vtk.vtkDataSetMapper()
            mapper.SetInputConnection(self._input_filter.get_output_port_by_name(category))

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            self._mappers[category] = mapper
            self._actors[category] = actor

        self._actors['element'].GetProperty().EdgeVisibilityOn()

    def set_renderer(self, renderer):
        if self._renderer is not None:
            self.remove_renderer()

        self._renderer = renderer

        for category in self._categories:
            self._renderer.AddActor(self._actors[category])

    def remove_renderer(self):
        for category in self._categories:
            self._renderer.RemoveActor(self._actors[category])

        self._renderer = None

    def get_actor_by_name(self, name):
        return self._actors[name]

    def get_mapper_by_name(self, name):
        return self._actors[name]

    def get_renderer(self):
        return self._renderer

    def get_input_filter(self):
        return self._input_filter