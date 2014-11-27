__author__ = 'Michael Redmond'

import vtk


# noinspection PyUnusedLocal
class DefaultInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, widget):

        self.widget = widget
        self.picker = vtk.vtkCellPicker()

        self.data = None

        self._left_mouse_down = False
        self._right_mouse_down = False
        self._middle_mouse_down = False
        self._should_it_render = False

        self.selectedMapper = vtk.vtkDataSetMapper()
        self.selectedActor = vtk.vtkActor()

        self.selectedActor.SetMapper(self.selectedMapper)

        self.actor_added = False

        self._last_selection = ''

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

    def on_left_button_up(self, obj, event):
        self.OnLeftButtonUp()
        self._left_mouse_down = False

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
        self.OnMouseWheelForward()

    def on_mouse_wheel_backward(self, obj, event):
        self.OnMouseWheelBackward()

    def on_mouse_move(self, obj, event):
        self.OnMouseMove()

        if self._left_mouse_down or self._right_mouse_down or self._middle_mouse_down:
            self._should_it_render = True
            selected = vtk.vtkUnstructuredGrid()
            self.selectedMapper.SetInputData(selected)
            self.selectedActor.SetMapper(self.selectedMapper)
            self.render()
            return

        pos = self.GetInteractor().GetEventPosition()

        if self.node_pick(pos):
            pass
        #elif self.cell_pick(pos):
        #    pass
        else:
            self.nothing_picked()

        self.render()

        return

    def render(self):
        if self._should_it_render:
            render_window = self.GetInteractor().GetRenderWindow()
            #render_window.GetRenderers().GetFirstRenderer().AddActor(self.selectedActor)

            if not self.actor_added:
                self.GetDefaultRenderer().AddActor(self.selectedActor)
                self.actor_added = True

            render_window.Render()

    def nothing_picked(self):
        selected = vtk.vtkUnstructuredGrid()
        self.selectedMapper.SetInputData(selected)
        #self.selectedActor.SetMapper(self.selectedMapper)

        self._should_it_render = True

        #render_window = self.GetInteractor().GetRenderWindow()
        #render_window.GetRenderers().GetFirstRenderer().RemoveActor(self.selectedActor)
        #render_window.Render()

    def node_pick(self, pos):

        self.picker.SetTolerance(0.005)
        self.picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        _id = self.picker.GetPointId()

        print _id

        if _id >= 0:

            if self._last_selection == 'Node %s' % str(_id):
                self._should_it_render = False
                return True

            self._last_selection = 'Node %s' % str(_id)

            ids = vtk.vtkIdTypeArray()
            ids.SetNumberOfComponents(1)
            ids.InsertNextValue(_id)

            selectionNode = vtk.vtkSelectionNode()
            selectionNode.SetFieldType(vtk.vtkSelectionNode.POINT)
            selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
            selectionNode.SetSelectionList(ids)

            selection = vtk.vtkSelection()
            selection.AddNode(selectionNode)

            extractSelection = vtk.vtkExtractSelection()
            extractSelection.SetInputData(0, self.widget.grid)
            extractSelection.SetInputData(1, selection)
            extractSelection.Update()

            selected = vtk.vtkUnstructuredGrid()
            selected.ShallowCopy(extractSelection.GetOutput())

            self.selectedMapper.SetInputData(selected)

            #self.selectedActor.SetMapper(self.selectedMapper)
            self.selectedActor.GetProperty().EdgeVisibilityOn()
            self.selectedActor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetPointSize(6)

            self._should_it_render = True
            return True
        else:
            self._should_it_render = False
            return False

    def cell_pick(self, pos):
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.005)
        picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        _id = picker.GetCellId()

        if _id != -1:

            if self._last_selection == 'Element %s' % str(_id):
                self._should_it_render = False
                return True

            self._last_selection = 'Element %s' % str(_id)

            ids = vtk.vtkIdTypeArray()
            ids.SetNumberOfComponents(1)
            ids.InsertNextValue(_id)

            selectionNode = vtk.vtkSelectionNode()
            selectionNode.SetFieldType(vtk.vtkSelectionNode.CELL)
            selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
            selectionNode.SetSelectionList(ids)

            selection = vtk.vtkSelection()
            selection.AddNode(selectionNode)

            extractSelection = vtk.vtkExtractSelection()
            extractSelection.SetInputData(0, self.widget.grid)
            extractSelection.SetInputData(1, selection)
            extractSelection.Update()

            selected = vtk.vtkUnstructuredGrid()
            selected.ShallowCopy(extractSelection.GetOutput())

            self.selectedMapper.SetInputData(selected)

            self.selectedActor.SetMapper(self.selectedMapper)
            self.selectedActor.GetProperty().EdgeVisibilityOn()
            self.selectedActor.GetProperty().SetColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetPointSize(6)

            self._should_it_render = True
            return True
        else:
            self._should_it_render = False
            return False