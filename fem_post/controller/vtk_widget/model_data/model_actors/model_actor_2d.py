__author__ = 'Michael Redmond'

import vtk


class ModelActor2D(object):
    def __init__(self):
        super(ModelActor2D, self).__init__()

        self.nodes = vtk.vtkActor2D()
        self.elements = vtk.vtkActor2D()
        self.mpcs = vtk.vtkActor2D()

        self.model_mapper_2d = None
        self.renderer = None

    def set_mapper(self, model_mapper_2d):

        self.model_mapper_2d = model_mapper_2d

        self.nodes.SetMapper(model_mapper_2d.nodes)
        self.elements.SetMapper(model_mapper_2d.elements)
        self.mpcs.SetMapper(model_mapper_2d.mpcs)

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