__author__ = 'Michael Redmond'

import vtk

from fem_post.application.vtk_widget.algorithms import GlobalIdFilter, SplitDataFilter


class SelectedPipelineHelper(object):
    def __init__(self, parent, renderer):
        super(SelectedPipelineHelper, self).__init__()

        self.parent = parent

        self.global_id_filter = GlobalIdFilter()

        self.split_data_filter = SplitDataFilter()
        self.split_data_filter.SetInputConnection(0, self.global_id_filter.GetOutputPort(0))

        self.node_mapper = vtk.vtkDataSetMapper()
        self.node_mapper.SetInputConnection(self.split_data_filter.node_port())

        self.node_actor = vtk.vtkActor()
        self.node_actor.SetMapper(self.node_mapper)
        self.node_actor.GetProperty().SetPointSize(6)
        self.node_actor.GetProperty().SetColor(0, 0.5, 0.5)
        self.node_actor.GetProperty().SetRepresentationToWireframe()
        self.node_actor.GetProperty().LightingOff()

        self.vertex_mapper = vtk.vtkDataSetMapper()
        self.vertex_mapper.SetInputConnection(self.split_data_filter.vertex_port())

        self.vertex_actor = vtk.vtkActor()
        self.vertex_actor.SetMapper(self.vertex_mapper)
        self.vertex_actor.GetProperty().SetPointSize(1)
        self.vertex_actor.GetProperty().SetRepresentationToWireframe()
        self.vertex_actor.GetProperty().LightingOff()

        self.element_mapper = vtk.vtkDataSetMapper()
        self.element_mapper.SetInputConnection(self.split_data_filter.element_port())

        self.element_actor = vtk.vtkActor()
        self.element_actor.SetMapper(self.element_mapper)
        self.element_actor.GetProperty().SetColor(0, 0.5, 0.5)
        self.element_actor.GetProperty().SetLineWidth(1)
        #self.element_actor.GetProperty().SetOpacity(0.5)
        self.element_actor.GetProperty().SetRepresentationToWireframe()
        self.element_actor.GetProperty().LightingOff()

        self.mpc_mapper = vtk.vtkDataSetMapper()
        self.mpc_mapper.SetInputConnection(self.split_data_filter.mpc_port())

        self.mpc_actor = vtk.vtkActor()
        self.mpc_actor.SetMapper(self.mpc_mapper)
        self.mpc_actor.GetProperty().SetPointSize(1)
        self.mpc_actor.GetProperty().SetRepresentationToWireframe()
        self.mpc_actor.GetProperty().LightingOff()

        self.renderer = None

        if renderer is not None:
            self.set_renderer(renderer)

    def set_renderer(self, renderer):
        if self.renderer is not None:
            self.remove_renderer()

        self.renderer = renderer

        self.renderer.AddActor(self.node_actor)
        self.renderer.AddActor(self.vertex_actor)
        self.renderer.AddActor(self.element_actor)
        self.renderer.AddActor(self.mpc_actor)

    def remove_renderer(self):
        self.renderer.RemoveActor(self.node_actor)
        self.renderer.RemoveActor(self.vertex_actor)
        self.renderer.RemoveActor(self.element_actor)
        self.renderer.RemoveActor(self.mpc_actor)

    def reset_data(self):
        self.global_id_filter.reset()

    def number_of_cells(self):
        return self.global_id_filter.GetOutputDataObject(0).GetNumberOfCells()

    def update_data(self, selection):

        self.global_id_filter.set_selection_list(selection)

        self.parent.render()

    def translate_actors(self, x, y, z):
        origin = list(self.node_actor.GetOrigin())
        origin[0] += x
        origin[1] += y
        origin[2] += z

        self.node_actor.SetOrigin(*origin)
        self.vertex_actor.SetOrigin(*origin)
        self.element_actor.SetOrigin(*origin)
        self.mpc_actor.SetOrigin(*origin)