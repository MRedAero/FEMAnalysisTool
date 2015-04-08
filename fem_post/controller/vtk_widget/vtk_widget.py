__author__ = 'Michael Redmond'

import vtk

#vtk.vtkAlgorithm.SetDefaultExecutivePrototype(vtk.vtkCompositeDataPipeline())

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from widgets import *
from interactor_styles import *
from algorithms import *
from vtk_globals import vtk_globals


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


class VTKWidget(object):
    def __init__(self, main_window):
        super(VTKWidget, self).__init__()

        self.renderer = vtk.vtkRenderer()
        self.renderer_picked = vtk.vtkRenderer()
        self.renderer_hovered = vtk.vtkRenderer()

        self.data_source = BDFDataSource()
        self.group_selections_ = vtk.vtkPolyData()
        self.group_filter = GroupFilter()
        self.visible_filter = VisibleFilter()

        self.main_pipeline = MainPipelineHelper(self.renderer)
        self.selected_pipeline = SelectedPipelineHelper(self, self.renderer_picked)
        self.hovered_pipeline = HoveredPipelineHelper(self, self.renderer_hovered)

        self.set_up_pipeline()
        self.set_up_view(main_window)

        self.visible_filter.add_callback(self.interactor_style.model_picker.set_data)

        ui = self.main_window.ui

        ui.left_click_combo.currentIndexChanged[str].connect(self.interactor_style.set_left_button)
        ui.middle_click_combo.currentIndexChanged[str].connect(self.interactor_style.set_middle_button)
        ui.right_click_combo.currentIndexChanged[str].connect(self.interactor_style.set_right_button)
        ui.ctrl_left_click_combo.currentIndexChanged[str].connect(self.interactor_style.set_ctrl_left_button)

        self.show_hide = False
        self.show = True

        self.bdf = None

        self.toggle_filter = vtk.vtkExtractSelection()
        self.toggle_filter.SetInputConnection(0, self.visible_filter.all_port())

        self.toggle_selection_node = vtk.vtkSelectionNode()
        self.toggle_selection_node.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)
        self.toggle_selection = vtk.vtkSelection()
        self.toggle_selection.AddNode(self.toggle_selection_node)

        self.toggle_filter.SetInputData(1, self.toggle_selection)

    def set_up_view(self, main_window):
        self.main_window = main_window
        self.interactor = QVTKRenderWindowInteractor(self.main_window.ui.frame)

        self.renderer.SetLayer(0)
        self.renderer.SetInteractive(1)
        #self.renderer.BackingStoreOn()

        self.renderer_picked.SetLayer(1)
        self.renderer_picked.SetInteractive(1)
        #self.renderer_picked.BackingStoreOn()

        self.renderer_hovered.SetLayer(2)
        self.renderer_hovered.SetInteractive(1)

        self.interactor.GetRenderWindow().SetNumberOfLayers(3)
        self.interactor.GetRenderWindow().AddRenderer(self.renderer_hovered)
        self.interactor.GetRenderWindow().AddRenderer(self.renderer_picked)
        self.interactor.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor.GetRenderWindow().SetAlphaBitPlanes(1)

        self.main_window.ui.vl.addWidget(self.interactor)

        self.iren = self.interactor.GetRenderWindow().GetInteractor()

        self.bg_color_1_default = (0, 0, 1)
        self.bg_color_2_default = (0.8, 0.8, 1)

        self.bg_color_1 = self.bg_color_1_default
        self.bg_color_2 = self.bg_color_2_default

        self.axes = CoordinateAxes(self.interactor)

        self.renderer.SetBackground(self.bg_color_1)
        self.renderer.SetBackground2(self.bg_color_2)
        self.renderer.GradientBackgroundOn()

        self.perspective = 0
        self.camera = vtk.vtkCamera()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()

        self.renderer_picked.SetActiveCamera(self.camera)
        self.renderer_hovered.SetActiveCamera(self.camera)

        self.interactor_style = DefaultInteractorStyle(self)
        self.interactor_style.set_default_renderer(self.renderer)
        #self.interactor_style.SetDefaultRenderer(self.renderer)

        self.interactor.SetInteractorStyle(self.interactor_style)

        self.interactor.Start()

        # http://www.paraview.org/Wiki/VTK/Examples/Python/Widgets/EmbedPyQt
        # http://www.vtk.org/pipermail/vtk-developers/2013-July/014005.html
        # see above why self.main_window.show() is done here

        self.main_window.show()
        self.iren.Initialize()

    def set_up_pipeline(self):

        self.group_selections = self.group_selections_.GetCellData()

        # this is temporary for now until grouping features are added
        self.group_selections.AddArray(self.data_source.default_group)

        self.group_filter.SetInputConnection(0, self.data_source.GetOutputPort(0))
        self.group_filter.set_group_selections(self.group_selections)

        self.visible_filter.SetInputConnection(0, self.group_filter.GetOutputPort(0))

        self.main_pipeline.split_data_filter.SetInputConnection(self.visible_filter.all_port())

        self.selected_pipeline.global_id_filter.SetInputConnection(self.visible_filter.all_port())

        self.hovered_pipeline.global_id_filter.SetInputConnection(self.visible_filter.all_port())

    def render(self):
        self.interactor.GetRenderWindow().Render()

    def set_bdf_data(self, bdf):
        self.data_source.set_bdf(bdf)
        self.data_source.Update()
        self.render()

    # needs to be renamed
    def toggle_visible(self):
        self.visible_filter.toggle_visible()
        self.render()

    # needs to be renamed
    def toggle_selected(self):
        # toggles selected between shown and hidden

        self.toggle_selection_node.SetSelectionList(self.interactor_style.model_picker.picked_selection.all_selection_vtk_array())
        self.toggle_selection_node.Modified()
        self.toggle_selection.Modified()
        self.toggle_filter.Modified()
        self.toggle_filter.Update()

        selected_data = self.toggle_filter.GetOutput()
        original_ids = selected_data.GetCellData().GetArray("original_ids")

        original_data = self.group_filter.GetOutputDataObject(0)
        visible_array = original_data.GetCellData().GetArray("visible")

        # TODO: speed this up using numpy?
        for i in xrange(original_ids.GetNumberOfTuples()):
            id = int(original_ids.GetValue(i))
            previous_value = int(visible_array.GetTuple1(id))
            visible_array.SetTuple1(id, -previous_value)

        self.visible_filter.Modified()
        self.render()

    def toggle_picking(self, entity_type, index=None):
        self.interactor_style.model_picker.toggle_picking(entity_type, index)

    def update_ui_selection(self, selection):
        self.main_window.ui.selection_box.setText(selection)

    def replace_selection_button(self):
        self.interactor_style.model_picker.picked_selection.selection_type = vtk_globals.SELECTION_REPLACE

    def append_selection_button(self):
        self.interactor_style.model_picker.picked_selection.selection_type = vtk_globals.SELECTION_APPEND

    def remove_selection_button(self):
        self.interactor_style.model_picker.picked_selection.selection_type = vtk_globals.SELECTION_REMOVE

    def single_pick_button(self):
        self.interactor_style.set_selection_type(vtk_globals.SELECTION_SINGLE)

    def box_pick_button(self):
        self.interactor_style.set_selection_type(vtk_globals.SELECTION_BOX)

    def poly_pick_button(self):
        self.interactor_style.set_selection_type(vtk_globals.SELECTION_POLY)