__author__ = 'Michael Redmond'

from controller.vtk_widget.utilities import *


class BoxPicker(object):
    def __init__(self, model_picker):
        super(BoxPicker, self).__init__()

        self.model_picker = model_picker

        self.box_picker = vtk.vtkExtractSelectedFrustum()

        self._start_position = [0, 0]
        self._end_position = [0, 0]
        self._pixel_array = vtk.vtkUnsignedCharArray()

        self._left_button_down = False
        self._ctrl_left_button_down = False
        self._right_button_down = False
        self._middle_button_down = False

        self._down_pos = None
        self._up_pos = None

        self.renderer = None

        self.reset_picking_box()

        self.ex = vtk.vtkExtractSelection()
        self.selection_node = vtk.vtkSelectionNode()
        self.selection_node.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)
        self.ex_selection = vtk.vtkSelection()
        self.ex_selection.AddNode(self.selection_node)

        self.ex.SetInputConnection(0, self.box_picker.GetOutputPort())
        self.ex.SetInputData(1, self.ex_selection)

        self._down_pos = None
        self._up_pos = None

        self.selection = None
        self.reset_selection()

        self.set_data()

    def add_renderer(self, renderer):
        if self.renderer is not None:
            self.remove_renderer()

        self.renderer = renderer
        self.renderer.AddActor2D(self.box_actor)
        self.model_picker.render()

    def remove_renderer(self):
        self.renderer.RemoveActor2D(self.box_actor)
        self.renderer = None

    def reset_selection(self):
        self.selection = {'Node': [],
                          'Element': [],
                          'MPC': [],
                          'Load': [],
                          'Disp': []}

    def set_data(self):
        data = self.model_picker.visible_filter.all_data()
        self.box_picker.SetInputData(data)

    def reset_box_and_picked_data(self):
        self.reset_picking_box()
        self.model_picker.reset_picked_data()

    def reset_picking_box(self):
        pass

    def begin_picking(self, interactor):

        self.ren_win = interactor.GetRenderWindow()
        self.ren_win_size = self.ren_win.GetSize()

        self._start_position[0] = interactor.GetEventPosition()[0]
        self._start_position[1] = interactor.GetEventPosition()[1]
        self._end_position[0] = self._start_position[0]
        self._end_position[1] = self._start_position[1]

        self._pixel_array.Reset()
        self._pixel_array.SetNumberOfComponents(4)
        self._pixel_array.SetNumberOfTuples(self.ren_win_size[0] * self.ren_win_size[1])

        self.ren_win.GetRGBACharPixelData(0, 0, self.ren_win_size[0] - 1, self.ren_win_size[1] - 1, 1,
                                          self._pixel_array)

        pos = interactor.GetEventPosition()

        self._down_pos = pos

    def end_picking(self, interactor):

        pos = interactor.GetEventPosition()

        self._up_pos = pos

        self._frustum = create_box_frustum(self._down_pos[0], self._down_pos[1],
                                           self._up_pos[0], self._up_pos[1], self.model_picker.get_renderer())

        self.box_picker.SetFrustum(self._frustum)

        self.something_picked()

    def something_picked(self):

        self.selection_node.SetSelectionList(self.model_picker.active_selections.selection_threshold())
        self.selection_node.Modified()
        self.ex_selection.Modified()

        self.box_picker.Modified()
        self.ex.Update()

        self.reset_picking_box()

        data = self.ex.GetOutput()

        global_ids = data.GetCellData().GetArray("global_ids")
        self.reset_selection()

        if global_ids is None:
            global_id_count = 0
        else:
            global_id_count = global_ids.GetNumberOfTuples()

        cell_type = vtk_globals.cell_type

        for i in xrange(global_id_count):
            id = global_ids.GetValue(i)

            type = cell_type(id)

            self.selection[type].append(id)

        self.model_picker.picked_selection.update_selection(self.selection)

    def mouse_move(self, interactor):

        self._end_position[0] = interactor.GetEventPosition()[0]
        self._end_position[1] = interactor.GetEventPosition()[1]
        self.ren_win_size = self.ren_win.GetSize()

        size = self.ren_win_size

        if self._end_position[0] > size[0] - 1:
            self._end_position[0] = size[0] - 1

        if self._end_position[0] < 0:
            self._end_position[0] = 0

        if self._end_position[1] > size[1] - 1:
            self._end_position[1] = size[1] - 1

        if self._end_position[1] < 0:
            self._end_position[1] = 0

        self._redraw_picking_box(interactor)

    def _redraw_picking_box(self, interactor):
        tmp_array = vtk.vtkUnsignedCharArray()
        tmp_array.DeepCopy(self._pixel_array)

        min = [0, 0]
        max = [0, 0]

        size = self.ren_win_size

        if self._start_position[0] <= self._end_position[0]:
            min[0] = self._start_position[0]
        else:
            min[0] = self._end_position[0]

        if min[0] < 0:
            min[0] = 0
        if min[0] >= size[0]:
            min[0] = size[0] - 1

        if self._start_position[1] <= self._end_position[1]:
            min[1] = self._start_position[1]
        else:
            min[1] = self._end_position[1]

        if min[1] < 0:
            min[1] = 0
        if min[1] >= size[1]:
            min[1] = size[1] - 1

        if self._end_position[0] > self._start_position[0]:
            max[0] = self._end_position[0]
        else:
            max[0] = self._start_position[0]

        if max[0] < 0:
            max[0] = 0
        if max[0] >= size[0]:
            max[0] = size[0] - 1

        if self._end_position[1] > self._start_position[1]:
            max[1] = self._end_position[1]
        else:
            max[1] = self._start_position[1]

        if max[1] < 0:
            max[1] = 0
        if max[1] >= size[1]:
            max[1] = size[1] - 1

        my_int = int

        for i in xrange(min[0], max[0] + 1):
            index1 = min[1] * size[0] + i
            tuple4 = tmp_array.GetTuple4(index1)
            tuple4 = map(my_int, tuple4)
            tuple4[0] = 255 ^ tuple4[0]
            tuple4[1] = 255 ^ tuple4[1]
            tuple4[2] = 255 ^ tuple4[2]
            tmp_array.SetTuple4(index1, *tuple4)

            index1 = max[1] * size[0] + i
            tuple4 = tmp_array.GetTuple4(index1)
            tuple4 = map(my_int, tuple4)
            tuple4[0] = 255 ^ tuple4[0]
            tuple4[1] = 255 ^ tuple4[1]
            tuple4[2] = 255 ^ tuple4[2]
            tmp_array.SetTuple4(index1, *tuple4)

        for i in xrange(min[1] + 1, max[1]):
            index1 = i*size[0] + min[0]
            tuple4 = tmp_array.GetTuple4(index1)
            tuple4 = map(my_int, tuple4)
            tuple4[0] = 255 ^ tuple4[0]
            tuple4[1] = 255 ^ tuple4[1]
            tuple4[2] = 255 ^ tuple4[2]
            tmp_array.SetTuple4(index1, *tuple4)

            index1 = i*size[0] + max[0]
            tuple4 = tmp_array.GetTuple4(index1)
            tuple4 = map(my_int, tuple4)
            tuple4[0] = 255 ^ tuple4[0]
            tuple4[1] = 255 ^ tuple4[1]
            tuple4[2] = 255 ^ tuple4[2]
            tmp_array.SetTuple4(index1, *tuple4)

        # print pixels

        interactor.GetRenderWindow().SetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, tmp_array, 0)
        interactor.GetRenderWindow().Frame()