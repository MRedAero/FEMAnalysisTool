__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore

from ..vtk_globals import *
from ..custom_pickers import *

selection_replace = 0
selection_append = 1
selection_remove = 2

selection_single = 0
selection_box = 1
selection_poly = 2


class PolyPlanePickerDataExtractor(object):
    """This is a helper class for PolyPlanePicker"""

    def __init__(self):
        super(PolyPlanePickerDataExtractor, self).__init__()

        self.input_data = None
        self.poly_plane = None

        self.extractor = vtk.vtkExtractGeometry()
        self.extractor.ExtractInsideOn()
        self.extractor.ExtractBoundaryCellsOn()

    def set_input_data(self, data):
        self.input_data = data

        if VTK_VERSION >= 6.0:
            self.extractor.SetInputData(self.input_data)
        else:
            self.extractor.SetInput(self.input_data)

        if self.poly_plane is not None:
            self.extractor.Update()

    def set_poly_plane(self, poly_plane):
        self.poly_plane = poly_plane

        self.extractor.SetImplicitFunction(self.poly_plane)

        if self.input_data is not None:
            self.extractor.Update()

    def get_output(self):
        return self.extractor.GetOutput()

    def update(self):
        if self.input_data is not None and self.poly_plane is not None:
            self.extractor.Update()


class DataExtractor(object):
    """This is a helper class for PolyPlanePicker"""

    def __init__(self):
        super(DataExtractor, self).__init__()

        self.input_data = None
        self.implicit_function = None

        self.extractor = vtk.vtkExtractGeometry()
        self.extractor.ExtractInsideOn()
        self.extractor.ExtractBoundaryCellsOn()

    def set_input_data(self, data):
        self.input_data = data

        if VTK_VERSION >= 6.0:
            self.extractor.SetInputData(self.input_data)
        else:
            self.extractor.SetInput(self.input_data)

        if self.implicit_function is not None:
            self.extractor.Update()

    def set_implicit_function(self, implicit_function):
        self.implicit_function = implicit_function

        self.extractor.SetImplicitFunction(self.implicit_function)

        if self.input_data is not None:
            self.extractor.Update()

    def get_output(self):
        return self.extractor.GetOutput()

    def update(self):
        if self.input_data is not None and self.implicit_function is not None:
            self.extractor.Update()


class ActiveSelections(QtCore.QObject):
    """This is a helper class for PolyPlanePicker"""

    selection_changed = QtCore.Signal()

    def __init__(self):
        super(ActiveSelections, self).__init__()

        self._nodes = True
        self._elements = True
        self._rbes = True

        self._points = True
        self._bars = True
        self._tris = True
        self._quads = True

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

        self.selection_changed.emit()

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        self._elements = value

        self._points = value
        self._bars = value
        self._tris = value
        self._quads = value

        self.selection_changed.emit()

    @property
    def rbes(self):
        return self._rbes

    @rbes.setter
    def rbes(self, value):
        self._rbes = value

        self.selection_changed.emit()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

        self.selection_changed.emit()

    @property
    def bars(self):
        return self._bars

    @bars.setter
    def bars(self, value):
        self._bars = value

        self.selection_changed.emit()

    @property
    def tris(self):
        return self._tris

    @tris.setter
    def tris(self, value):
        self._tris = value

        self.selection_changed.emit()

    @property
    def quads(self):
        return self._quads

    @quads.setter
    def quads(self, value):
        self._quads = value

        self.selection_changed.emit()


class GenericPicker(object):
    def __init__(self, poly_plane_picker):
        super(GenericPicker, self).__init__()

        self.poly_plane_picker = poly_plane_picker

    def connect_signals(self):
        interactor_style = self.poly_plane_picker.interactor_style

        interactor_style.signals.left_button_down.connect(self.left_button_down)
        interactor_style.signals.left_button_double_click.connect(self.left_button_double_click)
        interactor_style.signals.left_button_up.connect(self.left_button_up)
        interactor_style.signals.middle_button_down.connect(self.middle_button_down)
        interactor_style.signals.middle_button_up.connect(self.middle_button_up)
        interactor_style.signals.right_button_down.connect(self.right_button_down)
        interactor_style.signals.right_button_up.connect(self.right_button_up)
        interactor_style.signals.mouse_wheel_forward.connect(self.mouse_wheel_forward)
        interactor_style.signals.mouse_wheel_backward.connect(self.mouse_wheel_backward)
        interactor_style.signals.mouse_move.connect(self.mouse_move)

    def disconnect_signals(self):
        interactor_style = self.poly_plane_picker.interactor_style

        interactor_style.signals.left_button_down.disconnect(self.left_button_down)
        interactor_style.signals.left_button_double_click.disconnect(self.left_button_double_click)
        interactor_style.signals.left_button_up.disconnect(self.left_button_up)
        interactor_style.signals.middle_button_down.disconnect(self.middle_button_down)
        interactor_style.signals.middle_button_up.disconnect(self.middle_button_up)
        interactor_style.signals.right_button_down.disconnect(self.right_button_down)
        interactor_style.signals.right_button_up.disconnect(self.right_button_up)
        interactor_style.signals.mouse_wheel_forward.disconnect(self.mouse_wheel_forward)
        interactor_style.signals.mouse_wheel_backward.disconnect(self.mouse_wheel_backward)
        interactor_style.signals.mouse_move.disconnect(self.mouse_move)

    def left_button_down(self, obj, event, interactor):
        pass

    def left_button_double_click(self, obj, event, interactor):
        pass

    def left_button_up(self, obj, event, interactor):
        pass

    def middle_button_down(self, obj, event, interactor):
        pass

    def middle_button_up(self, obj, event, interactor):
        pass

    def right_button_down(self, obj, event, interactor):
        pass

    def right_button_up(self, obj, event, interactor):
        pass

    def mouse_wheel_forward(self, obj, event, interactor):
        pass

    def mouse_wheel_backward(self, obj, event, interactor):
        pass

    def mouse_move(self, obj, event, interactor):
        pass


class SinglePicker(GenericPicker):
    def __init__(self, poly_plane_picker):
        super(SinglePicker, self).__init__(poly_plane_picker)

        self.poly_plane_picker = poly_plane_picker
        """:type : PolyPlanePicker"""

        self.node_picker = vtkNodePicker()
        self.element_picker = vtkThruCellPicker()
        self.rbe_picker = vtkThruCellPicker()

        self.node_picker.SetTolerance(0.005)
        self.element_picker.SetTolerance(0.005)
        self.rbe_picker.SetTolerance(0.005)

        self._last_selection = None

        self._left_button_down = False
        self._right_button_down = False
        self._middle_button_down = False

    def set_data(self):
        data = self.poly_plane_picker.get_data()

        node_actor = self.poly_plane_picker.get_actors()['nodes']

        self.node_picker.add_pick_list(node_actor)
        self.element_picker.SetDataSet(data['elements'])
        self.rbe_picker.SetDataSet(data['rbes'])

        if data['elements'].GetNumberOfCells() > 0:
            self.element_picker.Update()
            self.element_picker.Modified()

        if data['rbes'].GetNumberOfCells() > 0:
            self.rbe_picker.Update()
            self.rbe_picker.Modified()

    def node_pick(self, pos):

        if self.poly_plane_picker.get_renderer() is None:
            return False

        self.node_picker.Pick(pos[0], pos[1], 0, self.poly_plane_picker.get_renderer())

        _id = self.node_picker.GetPointId()

        if _id >= 0:

            if self._last_selection == 'Node %s' % str(_id):
                return True

            self._last_selection = 'Node %s' % str(_id)

            self.poly_plane_picker.hover_data.Reset()
            self.poly_plane_picker.hover_data.ShallowCopy(self.node_picker.GetProjectedPoint())
            self.poly_plane_picker.hover_data.Modified()
            self.poly_plane_picker.render()

            return True
        else:
            return False


    def element_pick(self, pos):

        if self.poly_plane_picker.get_renderer() is None:
            return False

        self.element_picker.Pick(pos[0], pos[1], 0, self.poly_plane_picker.get_renderer())

        _id = self.element_picker.GetClosestCellId()

        if _id >= 0:

            if self._last_selection == 'Element %s' % str(_id):
                return True

            self._last_selection = 'Element %s' % str(_id)

            self.poly_plane_picker.hover_data.Reset()
            self.poly_plane_picker.hover_data.ShallowCopy(self.element_picker.GetClosestCellEdges())
            self.poly_plane_picker.hover_data.Modified()
            self.poly_plane_picker.render()

            return True
        else:
            return False

    def mouse_move(self, obj, event, interactor):

        if self._left_button_down or self._middle_button_down or self._right_button_down:
            self.no_selection()
            return

        pos = interactor.GetEventPosition()

        if self.poly_plane_picker.active_selections.nodes and self.node_pick(pos):
            pass
        elif self.poly_plane_picker.active_selections.elements and self.element_pick(pos):
            pass
        #elif self.poly_plane_picker.active_selections.rbes and self.pick(self.rbe_picker, pos):
        #    self.poly_plane_picker.render()
        else:
            self.no_selection()

    def no_selection(self):
        self._last_selection = None
        self.poly_plane_picker.hover_data.Reset()
        self.poly_plane_picker.hover_data.Modified()
        self.poly_plane_picker.render()

    def left_button_down(self, obj, event, interactor):
        self._left_button_down = True

    def left_button_double_click(self, obj, event, interactor):
        pass

    def left_button_up(self, obj, event, interactor):
        self._left_button_down = False

    def middle_button_down(self, obj, event, interactor):
        self._middle_button_down = True

    def middle_button_up(self, obj, event, interactor):
        self._middle_button_down = False

    def right_button_down(self, obj, event, interactor):
        self._right_button_down = True

    def right_button_up(self, obj, event, interactor):
        self._right_button_down = False

    def mouse_wheel_forward(self, obj, event, interactor):
        self.no_selection()

    def mouse_wheel_backward(self, obj, event, interactor):
        self.no_selection()


class BoxPicker(GenericPicker):
    def __init__(self, poly_plane_picker):
        super(BoxPicker, self).__init__(poly_plane_picker)

        self.poly_plane_picker = poly_plane_picker

    def left_button_down(self, obj, event, interactor):
        pass

    def left_button_double_click(self, obj, event, interactor):
        pass

    def left_button_up(self, obj, event, interactor):
        pass

    def middle_button_down(self, obj, event, interactor):
        pass

    def middle_button_up(self, obj, event, interactor):
        pass

    def right_button_down(self, obj, event, interactor):
        pass

    def right_button_up(self, obj, event, interactor):
        pass

    def mouse_wheel_forward(self, obj, event, interactor):
        pass

    def mouse_wheel_backward(self, obj, event, interactor):
        pass

    def mouse_move(self, obj, event, interactor):
        pass


class PolyPicker(GenericPicker):
    def __init__(self, poly_plane_picker):
        super(PolyPicker, self).__init__(poly_plane_picker)

        self.poly_plane_picker = poly_plane_picker

    def left_button_down(self, obj, event, interactor):
        pass

    def left_button_double_click(self, obj, event, interactor):
        pass

    def left_button_up(self, obj, event, interactor):
        pass

    def middle_button_down(self, obj, event, interactor):
        pass

    def middle_button_up(self, obj, event, interactor):
        pass

    def right_button_down(self, obj, event, interactor):
        pass

    def right_button_up(self, obj, event, interactor):
        pass

    def mouse_wheel_forward(self, obj, event, interactor):
        pass

    def mouse_wheel_backward(self, obj, event, interactor):
        pass

    def mouse_move(self, obj, event, interactor):
        pass


class PolyPlanePicker(object):
    def __init__(self):
        super(PolyPlanePicker, self).__init__()

        self.pipeline = None

        self.poly_points = vtk.vtkPoints()
        self.poly_line = vtk.vtkPolyLine()
        self.poly_data = vtk.vtkUnstructuredGrid()
        self.poly_plane = vtk.vtkPolyPlane()

        self.node_extractor = PolyPlanePickerDataExtractor()
        self.element_extractor = PolyPlanePickerDataExtractor()
        self.rbe_extractor = PolyPlanePickerDataExtractor()

        self.poly_data.SetPoints(self.poly_points)
        self.poly_data.InsertNextCell(self.poly_line.GetCellType(), self.poly_line.GetPointIds())
        self.poly_plane.SetPolyLine(self.poly_line)

        self.node_extractor.set_poly_plane(self.poly_plane)
        self.element_extractor.set_poly_plane(self.poly_plane)
        self.rbe_extractor.set_poly_plane(self.poly_plane)

        self.hover_data = vtk.vtkPolyData()
        self.selected_data = vtk.vtkUnstructuredGrid()

        self.hover_mapper = vtk.vtkPolyDataMapper()
        self.selected_mapper = vtk.vtkDataSetMapper()

        if VTK_VERSION >= 6.0:
            self.hover_mapper.SetInputData(self.hover_data)
            self.selected_mapper.SetInputData(self.selected_data)
        else:
            self.hover_mapper.SetInput(self.hover_data)
            self.selected_mapper.SetInput(self.selected_data)

        self.hover_actor = vtk.vtkActor()
        self.selected_actor = vtk.vtkActor()

        self.hover_actor.GetProperty().EdgeVisibilityOn()
        self.hover_actor.GetProperty().SetColor(0.5, 0.5, 0)
        self.hover_actor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
        self.hover_actor.GetProperty().SetLineWidth(3)
        #self.hover_actor.GetProperty().SetOpacity(0.5)
        self.hover_actor.GetProperty().SetPointSize(6)

        self.hover_actor.SetMapper(self.hover_mapper)
        self.selected_actor.SetMapper(self.selected_mapper)

        self.selection_option = selection_replace

        self.active_selections = ActiveSelections()
        self.active_selections.selection_changed.connect(self.active_selections_changed)

        self.selection_type = 0

        self.set_selection_type(selection_single)

        self.interactor_style = None

        self.single_picker = SinglePicker(self)
        self.box_picker = BoxPicker(self)
        self.poly_picker = PolyPicker(self)

    def set_pipeline(self, pipeline):
        if self.pipeline is not None:
            self.pipeline.data_updated.disconnect(self.update_data)
            self.pipeline.get_renderer().RemoveActor(self.hover_actor)
            self.pipeline.get_renderer().RemoveActor(self.selected_actor)

        self.pipeline = pipeline
        """:type: fem_post.controller.vtk_widget.pipelines.DataPipeline"""

        self.pipeline.data_updated.connect(self.update_data)
        self.pipeline.get_renderer().AddActor(self.hover_actor)
        self.pipeline.get_renderer().AddActor(self.selected_actor)

        self.single_picker.node_picker.Renderer = self.get_renderer()

        self.update_data()

    def update_data(self):
        if self.pipeline is None:
            return

        data = self.get_data()

        self.node_extractor.set_input_data(data['nodes'])
        self.element_extractor.set_input_data(data['elements'])
        self.rbe_extractor.set_input_data(data['rbes'])

        self.single_picker.set_data()

    def get_data(self):
        return {'nodes': self.pipeline.node_mapper.GetInput(),
                'elements': self.pipeline.element_mapper.GetInput(),
                'rbes': self.pipeline.rbe_mapper.GetInput()}

    def get_actors(self):
        return {'nodes': self.pipeline.node_actor,
                'elements': self.pipeline.element_actor,
                'rbes': self.pipeline.rbe_actor}

    def get_renderer(self):
        if self.pipeline is None:
            return None

        return self.pipeline.get_renderer()

    def reset(self):
        self.poly_points.Reset()
        self.poly_line.Reset()

        self.hover_data.Reset()
        self.selected_data.Reset()

    def set_interactor_style(self, interactor_style):
        if self.interactor_style is not None:
            self.disconnect_interactor_style_signals()

        self.interactor_style = interactor_style

        self.connect_interactor_style_signals()

    def set_selection_type(self, value):
        if value == self.selection_type:
            return

        self.disconnect_interactor_style_signals()

        self.selection_type = value

        self.connect_interactor_style_signals()

    def connect_interactor_style_signals(self):
        if self.interactor_style is not None:
            if self.selection_type == selection_single:
                self.single_picker.connect_signals()
            elif self.selection_type == selection_box:
                self.box_picker.connect_signals()
            elif self.selection_type == selection_poly:
                self.poly_picker.connect_signals()

    def disconnect_interactor_style_signals(self):
        if self.interactor_style is not None:
            if self.selection_type == selection_single:
                self.single_picker.disconnect_signals()
            elif self.selection_type == selection_box:
                self.box_picker.disconnect_signals()
            elif self.selection_type == selection_poly:
                self.poly_picker.disconnect_signals()

    def active_selections_changed(self):
        pass

    def render(self):
        self.interactor_style.GetInteractor().GetRenderWindow().Render()