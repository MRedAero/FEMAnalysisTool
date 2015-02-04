__author__ = 'Michael Redmond'

from .abstract_picker import AbstractPicker
from ...custom_pickers import *
from .active_selections import ActiveSelections
from ...vtk_globals import *
from ...utilities import *


class BoxPicker(AbstractPicker):
    def __init__(self, model_picker):
        super(BoxPicker, self).__init__(model_picker)

        self.poly_points = vtk.vtkPoints()
        self.poly_line = vtk.vtkPolyLine()
        self.poly_plane = vtk.vtkPolyPlane()

        self.cell_array = vtk.vtkCellArray()

        self.poly_plane.SetPolyLine(self.poly_line)

        self.node_picker = vtk.vtkExtractGeometry()
        self.element_picker = vtk.vtkExtractGeometry()
        self.rbe_picker = vtk.vtkExtractGeometry()

        self.node_picker.ExtractBoundaryCellsOn()
        self.element_picker.ExtractBoundaryCellsOn()
        self.rbe_picker.ExtractBoundaryCellsOn()

        self.node_picker.ExtractInsideOn()
        self.element_picker.ExtractInsideOn()
        self.rbe_picker.ExtractInsideOn()

        self._picking_box = vtk.vtkPlanes()

        self.node_picker.SetImplicitFunction(self.poly_plane)
        self.element_picker.SetImplicitFunction(self.poly_plane)
        self.rbe_picker.SetImplicitFunction(self.poly_plane)

        self.box_points = vtk.vtkPoints()

        self.box_poly = vtk.vtkPolyData()
        self.box_poly.SetPoints(self.box_points)

        self.box_mapper = vtk.vtkPolyDataMapper()
        self.box_mapper.SetInputData(self.box_poly)
        self.box_actor = vtk.vtkActor()
        self.box_actor.SetMapper(self.box_mapper)
        self.box_actor.GetProperty().SetPointSize(20)

        self._added = False

        self._left_button_down = False
        self._ctrl_left_button_down = False
        self._right_button_down = False
        self._middle_button_down = False

        self._picking_active = False

        self._down_pos = None
        self._up_pos = None
        self._pos1 = None
        self._pos2 = None
        self._pos3 = None
        self._pos4 = None

        self.selection = None
        self.reset_selection()

    def reset_selection(self):
        self.selection = {'nodes': [],
                          'elements': [],
                          'mpcs': [],
                          'loads': [],
                          'disps': []}

    def set_data(self):
        data = self.model_picker.get_data()

        if VTK_VERSION >= 6.0:
            self.node_picker.SetInputData(data['nodes'])
            self.element_picker.SetInputData(data['elements'])
            self.rbe_picker.SetInputData(data['rbes'])
        else:
            self.node_picker.SetInput(data['nodes'])
            self.element_picker.SetInput(data['elements'])
            self.rbe_picker.SetInput(data['rbes'])

        self.node_picker.Update()
        self.node_picker.Modified()

        self.element_picker.Update()
        self.element_picker.Modified()

        self.rbe_picker.Update()
        self.rbe_picker.Modified()

    def picking_active(self):
        return self._picking_active

    def begin_picking(self, pos):
        self._picking_active = True
        self._down_pos = pos

        self._pos1 = display_to_world(self._down_pos, self.model_picker.get_renderer(), .001)

        self.poly_points.Reset()

        self.poly_points.InsertNextPoint(self._pos1[:3])
        self.poly_points.InsertNextPoint(self._pos1[:3])
        self.poly_points.InsertNextPoint(self._pos1[:3])
        self.poly_points.InsertNextPoint(self._pos1[:3])

        self.reset_hover_data()

        self.model_picker.hover_data.SetPoints(self.poly_points)

        ids = self.poly_line.GetPointIds()
        ids.SetNumberOfIds(4)
        ids.SetId(0, 0)
        ids.SetId(1, 1)
        ids.SetId(2, 2)
        ids.SetId(3, 3)

        self.cell_array.Reset()
        self.cell_array.InsertNextCell(self.poly_line)
        self.model_picker.hover_data.SetPolys(self.cell_array)

    def end_picking(self, pos):

        if not self._added:
            self.model_picker.get_renderer().AddActor(self.box_actor)
            self._added = True

        self._picking_active = False
        self._up_pos = pos

        self._frustum = create_box_frustum(self._down_pos[0], self._down_pos[1],
                                     self._up_pos[0], self._up_pos[1], self.model_picker.get_renderer())

        print self._frustum

        #print self._picking_box

        self.poly_plane.SetPolyLine(self.poly_line)

       #print self.poly_plane

        self.node_picker.SetImplicitFunction(self._frustum)
        self.element_picker.SetImplicitFunction(self._frustum)
        self.rbe_picker.SetImplicitFunction(self._frustum)

        self.node_picker.Update()
        self.node_picker.Modified()

        self.element_picker.Update()
        self.element_picker.Modified()

        self.rbe_picker.Update()
        self.rbe_picker.Modified()

        #print self.element_picker.GetOutput().GetNumberOfCells()

        self.reset_hover_data()

        self.something_picked()

    def mouse_move(self, obj, event, interactor, action):

        should_pick = True

        if not self.picking_active():
            if self._left_button_down or self._ctrl_left_button_down or \
                    self._middle_button_down or self._right_button_down:
                self.reset_hover_and_selected_data()
            should_pick = False

        action()

        if not should_pick:
            return

        pos = interactor.GetEventPosition()

        self._pos3 = display_to_world(pos, self.model_picker.get_renderer(), .001)
        self._pos2 = display_to_world([pos[0], self._down_pos[1]], self.model_picker.get_renderer(), .001)
        self._pos4 = display_to_world([self._down_pos[0], pos[1]], self.model_picker.get_renderer(), .001)

        self.poly_points.SetPoint(1, self._pos2[:3])
        self.poly_points.SetPoint(2, self._pos3[:3])
        self.poly_points.SetPoint(3, self._pos4[:3])

        self.poly_points.Modified()
        self.poly_line.Modified()
        self.cell_array.Modified()
        self.model_picker.hover_data.Modified()

        self.model_picker.render()

    def reset_hover_data(self, do_not_render=False):
        #return
        self.model_picker.hover_data.Reset()
        self.model_picker.hover_data.Modified()

        if not do_not_render:
            self.model_picker.render()

    def reset_hover_and_selected_data(self):
        #return
        self.reset_hover_data(True)
        self.model_picker.reset_selected_data()

    def try_pick(self):
        if self._down_pos == self._up_pos:
            self.something_picked()
        else:
            self.model_picker.update_selection_data()

    def left_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._left_button_down = True

        if picking_is_active:
            self.begin_picking(interactor.GetEventPosition())

    def left_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._left_button_down = False

        if picking_is_active:
            self.end_picking(interactor.GetEventPosition())
        else:
            self.model_picker.update_selection_data()

    def ctrl_left_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._ctrl_left_button_down = True

        if picking_is_active:
            self.begin_picking(interactor.GetEventPosition())

    def ctrl_left_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._ctrl_left_button_down = False

        if picking_is_active:
            self.end_picking(interactor.GetEventPosition())
        else:
            self.model_picker.update_selection_data()

    def left_button_double_click(self, obj, event, interactor, action):
        pass

    def middle_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._middle_button_down = True

        if picking_is_active:
            self.begin_picking(interactor.GetEventPosition())

    def middle_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._middle_button_down = False

        if picking_is_active:
            self.end_picking(interactor.GetEventPosition())
        else:
            self.model_picker.update_selection_data()

    def right_button_down(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._right_button_down = True

        if picking_is_active:
            self.begin_picking(interactor.GetEventPosition())

    def right_button_up(self, obj, event, interactor, action, picking_is_active=False):
        if callable(action):
            action()

        self._right_button_down = False

        if picking_is_active:
            self.end_picking(interactor.GetEventPosition())
        else:
            self.model_picker.update_selection_data()

    def mouse_wheel_forward(self, obj, event, interactor, action):
        self.reset_hover_and_selected_data()
        action()
        self.model_picker.update_selection_data()

    def mouse_wheel_backward(self, obj, event, interactor, action):
        self.reset_hover_and_selected_data()
        action()
        self.model_picker.update_selection_data()

    def set_picking(self, active_selections):

        return

        self.node_picker.set_picking(VTK_VERTEX, active_selections.nodes)

        self.element_picker.set_picking(VTK_VERTEX, active_selections.points)
        self.element_picker.set_picking(VTK_LINE, active_selections.bars)
        self.element_picker.set_picking(VTK_TRI, active_selections.tris)
        self.element_picker.set_picking(VTK_QUAD, active_selections.quads)

        self.rbe_picker.set_picking(VTK_POLY_LINE, active_selections.rbes)

    def something_picked(self):
        self.reset_selection()

        data = self.element_picker.GetOutput().GetCellData()
        global_ids = data.GetGlobalIds()
        selection = []
        for i in xrange(global_ids.GetNumberOfTuples()):
            selection.append(str(int(round(float(global_ids.GetValue(i)), 0))))

        self.selection['elements'] = selection

        data = self.node_picker.GetOutput().GetCellData()
        global_ids = data.GetGlobalIds()
        selection = []
        for i in xrange(global_ids.GetNumberOfTuples()):
            selection.append(str(int(round(float(global_ids.GetValue(i)), 0))))

        self.selection['nodes'] = selection

        self.model_picker.selection_list.update_selection(self.selection)