__author__ = 'Michael Redmond'

import vtk
from ..custom_pickers import vtkThruCellPicker, vtkNodePicker


# noinspection PyUnusedLocal
class DefaultInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, widget):

        self.down_pos = [0, 0, 0]
        self.up_pos = [0, 0, 0]

        self.widget = widget
        self.point_picker = vtkNodePicker()
        self.point_data_set = False
        self.cell_picker = vtkThruCellPicker()
        self.cell_data_set = False

        self._left_mouse_down = False
        self._right_mouse_down = False
        self._middle_mouse_down = False
        self._should_it_render = False

        self.selectedMapper = vtk.vtkDataSetMapper()
        self.selectedActor = vtk.vtkActor()

        self.selectionNode = vtk.vtkSelectionNode()
        self.selection = vtk.vtkSelection()
        self.extractSelection = vtk.vtkExtractSelection()

        self.selectedActor.SetMapper(self.selectedMapper)

        self.actor_added = False

        self._last_selection = 'nothing'

        self.AddObserver("MouseMoveEvent", self.on_mouse_move)
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_down)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_up)
        self.AddObserver("MiddleButtonPressEvent", self.on_middle_button_down)
        self.AddObserver("MiddleButtonReleaseEvent", self.on_middle_button_up)
        self.AddObserver("RightButtonPressEvent", self.on_right_button_down)
        self.AddObserver("RightButtonReleaseEvent", self.on_right_button_up)
        self.AddObserver("MouseWheelForwardEvent", self.on_mouse_wheel_forward)
        self.AddObserver("MouseWheelBackwardEvent", self.on_mouse_wheel_backward)

    def on_left_button_down(self, obj, event):
        self.OnLeftButtonDown()
        self._left_mouse_down = True

        self.down_pos = self.GetInteractor().GetEventPosition()

    def on_left_button_up(self, obj, event):
        self.OnLeftButtonUp()
        self._left_mouse_down = False

        self.up_pos = self.GetInteractor().GetEventPosition()

        if self.down_pos == self.up_pos and self._last_selection != 'nothing':
            # these aren't actual node and element numbers
            msg_box = self.widget.main_window.ui.txt_msg
            msg_box.setPlainText(msg_box.toPlainText() + self._last_selection + '\n')

    def on_middle_button_down(self, obj, event):
        self.OnMiddleButtonDown()
        self._middle_mouse_down = True

    def on_middle_button_up(self, obj, event):
        self.OnMiddleButtonUp()
        self._middle_mouse_down = False

    def on_right_button_down(self, obj, event):
        self.OnRightButtonDown()
        self._right_mouse_down = True

    def on_right_button_up(self, obj, event):
        self.OnRightButtonUp()
        self._right_mouse_down = False

    def on_mouse_wheel_forward(self, obj, event):
        if self.actor_added:
            self.GetDefaultRenderer().RemoveActor(self.selectedActor)
            self.actor_added = False
        self.OnMouseWheelForward()
        self._last_selection = 'nothing'

    def on_mouse_wheel_backward(self, obj, event):
        if self.actor_added:
            self.GetDefaultRenderer().RemoveActor(self.selectedActor)
            self.actor_added = False
        self.OnMouseWheelBackward()
        self._last_selection = 'nothing'

    def on_mouse_move(self, obj, event):
        self.OnMouseMove()

        if self._left_mouse_down or self._right_mouse_down or self._middle_mouse_down:
            self._should_it_render = True
            if self.actor_added:
                self.GetDefaultRenderer().RemoveActor(self.selectedActor)
                self.actor_added = False
            self.render()
            return

        pos = self.GetInteractor().GetEventPosition()

        if self.node_pick(pos):
            pass
        elif self.cell_pick(pos):
            pass
        else:
            self.nothing_picked()

        self.render()

        return

    def render(self):
        if self._should_it_render:
            render_window = self.GetInteractor().GetRenderWindow()
            render_window.Render()

    def nothing_picked(self):
        if self.actor_added:
            self.GetDefaultRenderer().RemoveActor(self.selectedActor)
            self.actor_added = False

        if self._last_selection == "nothing":
            self._should_it_render = False
            return

        self._last_selection = "nothing"
        self._should_it_render = True

    def node_pick(self, pos):
        if self.widget.grid is None:
            return False

        self.point_picker.SetTolerance(0.0035)
        self.point_picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        if not self.point_data_set:
            self.point_picker.AddPickList(self.widget.cell_actor)
            self.point_picker.Renderer = self.GetDefaultRenderer()
            self.point_data_set = True
            self.point_picker.PickFromListOn()

        _id = self.point_picker.GetPointId()

        if _id >= 0:

            if self._last_selection == 'Node %s' % str(_id):
                self._should_it_render = False
                return True

            self._last_selection = 'Node %s' % str(_id)

            self.selectedMapper.SetInputData(self.point_picker.GetProjectedPoint())

            self.selectedActor.GetProperty().EdgeVisibilityOn()
            self.selectedActor.GetProperty().SetColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetLineWidth(3)
            self.selectedActor.GetProperty().SetOpacity(0.5)
            self.selectedActor.GetProperty().SetPointSize(6)

            if not self.actor_added:
                self.GetDefaultRenderer().AddActor(self.selectedActor)
                self.actor_added = True

            self._should_it_render = True

            #print "cell pick %d = %d\n" % (self.cell_pick_count, _id)

            return True
        else:
            return False

    def cell_pick(self, pos):
        if self.widget.grid is None:
            return False

        if not self.cell_data_set:
            self.cell_picker.SetDataSet(self.widget.grid)
            self.cell_data_set = True

        self.cell_picker.BuildLocator()
        self.cell_picker.SetTolerance(0.005)
        self.cell_picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        _id = self.cell_picker.GetClosestCellId()

        if _id >= 0:

            if self._last_selection == 'Element %s' % str(_id):
                self._should_it_render = False
                return True

            self._last_selection = 'Element %s' % str(_id)

            self.selectedMapper.SetInputData(self.cell_picker.GetClosestCellEdges())

            self.selectedActor.GetProperty().EdgeVisibilityOn()
            #self.selectedActor.GetProperty().SetColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetOpacity(0.5)
            self.selectedActor.GetProperty().SetLineWidth(3)
            self.selectedActor.GetProperty().SetPointSize(6)

            if not self.actor_added:
                self.GetDefaultRenderer().AddActor(self.selectedActor)
                self.actor_added = True

            self._should_it_render = True
            return True
        else:
            return False