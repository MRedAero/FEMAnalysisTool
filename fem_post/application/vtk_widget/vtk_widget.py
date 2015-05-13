__author__ = 'Michael Redmond'

import vtk

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from base_app.simple_pubsub import pub
from base_app.utilities import BaseObject

from fem_post.application.vtk_widget import vtk_globals
from fem_post.application.vtk_widget.algorithms import (BDFDataSource, VisibleFilter, GroupFilter)
from fem_post.application.vtk_widget.interactor_styles import DefaultInteractorStyle
from fem_post.application.vtk_widget.pipelines import \
    (MainPipelineHelper, SelectedPipelineHelper, HoveredPipelineHelper)
from fem_post.application.vtk_widget.widgets import CoordinateAxes


class VTKWidget(BaseObject):
    def __new__(cls, *args, **kwargs):
        instance = BaseObject.__new__(cls, *args, **kwargs)

        if "_actions" not in cls.__dict__:
            cls._actions = {'left_down': 'rotate_begin',
                            'ctrl_left_down': None,
                            'middle_down': 'pan_begin',
                            'right_down': 'zoom_begin',
                            'left_up': 'rotate_end',
                            'ctrl_left_up': None,
                            'middle_up': 'pan_end',
                            'right_up': 'zoom_end'}

        if "_picking" not in cls.__dict__:
            cls._picking = {'left_down': False,
                            'ctrl_left_down': True,
                            'middle_down': False,
                            'right_down': False,
                            'left_up': False,
                            'ctrl_left_up': True,
                            'middle_up': False,
                            'right_up': False}

        return instance

    @classmethod
    def reset_picking(cls):
        cls._picking = {'left_down': False,
                        'ctrl_left_down': False,
                        'middle_down': False,
                        'right_down': False,
                        'left_up': False,
                        'ctrl_left_up': False,
                        'middle_up': False,
                        'right_up': False}

    @classmethod
    def set_button_action(cls, button, action):
        """

        :param button:
        :param action:
        :type button: str
        :type action: str
        :return:
        """

        button = button.upper()
        action = action.upper()

        if button == 'LEFT':
            down = 'left_down'
            up = 'left_up'
        elif button == 'RIGHT':
            down = 'right_down'
            up = 'right_up'
        elif button == 'MIDDLE':
            down = 'middle_down'
            up = 'middle_up'
        elif button == 'CTRL_LEFT':
            down = 'ctrl_left_down'
            up = 'ctrl_left_up'
        else:
            return

        picking = False

        if action == 'ROTATE':
            begin = 'rotate_begin'
            end = 'rotate_end'
        elif action == 'PAN':
            begin = 'pan_begin'
            end = 'pan_end'
        elif action == 'ZOOM':
            begin = 'zoom_begin'
            end = 'zoom_end'
        elif action == 'SELECT':
            begin = None
            end = None
            picking = True
        else:
            return

        cls._actions[down] = begin
        cls._actions[up] = end

        if picking:
            cls.reset_picking()
            cls._picking[down] = picking
            cls._picking[up] = picking

        for instance in cls._instances:
            instance.interactor_style.set_button_actions(cls._actions, cls._picking)

    def __init__(self, main_window):
        super(VTKWidget, self).__init__()

        self._parent = main_window

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

        self.interactor_style.set_button_actions(self._actions, self._picking)

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

        #self.set_rotation_center(1000, 0, 0)

    def set_file(self, file):
        self.data_source.set_file(file)
        self.data_source.Update()
        self.render()

    def get_parent(self):
        return self._parent

    def initialize(self):
        self.iren.Initialize()

    def set_up_view(self, main_window):
        self.main_window = main_window

        self.interactor = QVTKRenderWindowInteractor(main_window)

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

        try:
            self.main_window.ui.vl.addWidget(self.interactor)
        except AttributeError:
            self.main_window.layout().addWidget(self.interactor)

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
        pos = self.camera.GetPosition()
        focal = self.camera.GetFocalPoint()
        self.camera_delta = [pos[0]-focal[0], pos[1]-focal[1], pos[2]-focal[2]]

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

        #try:
        #    self.main_window.show()
        #except AttributeError:
        #    print "can't show main_window"

        #self.iren.Initialize()

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

    def switch_view(self):
        self.visible_filter.toggle_visible()
        self.render()

    def show_hide_selection(self):
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

        if original_ids is None:
            return

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
        pub.publish("vtk.set_selection_box", selection)

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

    def unload(self):
        # this is required so that the vtk widget will release its memory
        #  this gives an error sometimes because main_window is None

        self.main_window.layout().removeWidget(self.interactor)
        self.interactor.Finalize()
        self.main_window = None
        self._parent = None

    def translate_actors(self, x, y, z):
        self.main_pipeline.translate_actors(x, y, z)
        self.selected_pipeline.translate_actors(x, y, z)
        self.hovered_pipeline.translate_actors(x, y, z)
        #new_pos = list(self.camera_delta)
        #new_pos[0] += x
        #new_pos[1] += y
        #new_pos[2] += z

        #self.camera.SetPosition(*new_pos)