__author__ = 'Michael Redmond'

import vtk

from fem_post.application.vtk_widget.algorithms import GlobalIdFilter


class HoveredPipelineHelper(object):
    def __init__(self, parent, renderer):
        super(HoveredPipelineHelper, self).__init__()

        self.parent = parent

        self.global_id_filter = GlobalIdFilter()

        self.mapper = vtk.vtkDataSetMapper()
        self.mapper.SetInputConnection(self.global_id_filter.GetOutputPort(0))

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)

        self.actor.GetProperty().SetColor(0.5, 0.5, 0)
        self.actor.GetProperty().SetLineWidth(2)
        self.actor.GetProperty().SetPointSize(6)
        self.actor.GetProperty().SetRepresentationToWireframe()
        self.actor.GetProperty().LightingOff()

        self.renderer = None

        if renderer is not None:
            self.set_renderer(renderer)

    def set_renderer(self, renderer):
        if self.renderer is not None:
            self.remove_renderer()

        self.renderer = renderer

        self.renderer.AddActor(self.actor)

    def remove_renderer(self):
        self.renderer.RemoveActor(self.actor)

    def reset_data(self):
        self.global_id_filter.reset()

    def number_of_cells(self):
        return self.global_id_filter.GetOutputDataObject(0).GetNumberOfCells()

    def update_data(self, selection, pick_type):

        self.global_id_filter.set_selection_list(selection)

        self.parent.render()

    def translate_actors(self, x, y, z):
        origin = list(self.actor.GetOrigin())
        origin[0] += x
        origin[1] += y
        origin[2] += z

        self.actor.SetOrigin(*origin)