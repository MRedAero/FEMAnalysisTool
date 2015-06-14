__author__ = 'Michael Redmond'

import vtk

from fem_post.application.vtk_widget.algorithms import SplitDataFilter


class MainPipelineHelper(object):
    def __init__(self, renderer):
        super(MainPipelineHelper, self).__init__()

        self.split_data_filter = SplitDataFilter()

        self.node_mapper = vtk.vtkDataSetMapper()
        self.node_mapper.SetInputConnection(self.split_data_filter.node_port())

        self.node_actor = vtk.vtkActor()
        self.node_actor.SetMapper(self.node_mapper)

        self.vertex_mapper = vtk.vtkDataSetMapper()
        self.vertex_mapper.SetInputConnection(self.split_data_filter.vertex_port())

        self.vertex_actor = vtk.vtkActor()
        self.vertex_actor.SetMapper(self.vertex_mapper)

        self.element_mapper = vtk.vtkDataSetMapper()
        self.element_mapper.SetInputConnection(self.split_data_filter.element_port())

        self.element_actor = vtk.vtkActor()
        self.element_actor.SetMapper(self.element_mapper)
        self.element_actor.GetProperty().EdgeVisibilityOn()

        self.mpc_mapper = vtk.vtkDataSetMapper()
        self.mpc_mapper.SetInputConnection(self.split_data_filter.mpc_port())

        self.mpc_actor = vtk.vtkActor()
        self.mpc_actor.SetMapper(self.mpc_mapper)

        self.force_mapper = vtk.vtkDataSetMapper()
        self.force_mapper.SetInputConnection(self.split_data_filter.force_port())

        self.force_actor = vtk.vtkActor()
        self.force_actor.SetMapper(self.force_mapper)

        self.disp_mapper = vtk.vtkDataSetMapper()
        self.disp_mapper.SetInputConnection(self.split_data_filter.disp_port())

        self.disp_actor = vtk.vtkActor()
        self.disp_actor.SetMapper(self.disp_mapper)

        self.coord_mapper = vtk.vtkDataSetMapper()
        self.coord_mapper.SetInputConnection(self.split_data_filter.coord_port())

        self.coord_actor = vtk.vtkActor()
        self.coord_actor.SetMapper(self.coord_mapper)

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
        self.renderer.AddActor(self.force_actor)
        self.renderer.AddActor(self.disp_actor)
        self.renderer.AddActor(self.coord_actor)

    def remove_renderer(self):
        self.renderer.RemoveActor(self.node_actor)
        self.renderer.RemoveActor(self.vertex_actor)
        self.renderer.RemoveActor(self.element_actor)
        self.renderer.RemoveActor(self.mpc_actor)
        self.renderer.RemoveActor(self.force_actor)
        self.renderer.RemoveActor(self.disp_actor)
        self.renderer.RemoveActor(self.coord_actor)