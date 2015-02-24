__author__ = 'Michael Redmond'

import vtk


class ModelActor(object):
    def __init__(self):
        super(ModelActor, self).__init__()

        self.nodes = vtk.vtkActor()
        self.elements = vtk.vtkActor()
        self.mpcs = vtk.vtkActor()

        self.model_mapper = None
        self.renderer = None

    def set_mapper(self, model_mapper):

        self.model_mapper = model_mapper

        self.nodes.SetMapper(model_mapper.nodes)
        self.elements.SetMapper(model_mapper.elements)
        self.mpcs.SetMapper(model_mapper.mpcs)

    def set_renderer(self, renderer):
        self.renderer = renderer

        self.renderer.AddActor(self.nodes)
        self.renderer.AddActor(self.elements)
        self.renderer.AddActor(self.mpcs)

    def remove_renderer(self):
        if self.renderer is None:
            return

        self.renderer.RemoveViewProp(self.nodes)
        self.renderer.RemoveViewProp(self.elements)
        self.renderer.RemoveViewProp(self.mpcs)

        self.renderer = None