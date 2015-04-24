__author__ = 'Michael Redmond'

from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from fem_post.application.vtk_widget.utilities import *
from fem_post.application.vtk_widget.algorithms import PolyPickFilter


class HelperFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
                                        nInputPorts=1, inputType='vtkPolyData',
                                        nOutputPorts=1, outputType='vtkPolyData')

        self.renderer = None

    def set_renderer(self, renderer):
        self.renderer = renderer

    def RequestData(self, request, inInfo, outInfo):
        inp = vtk.vtkPolyData.GetData(inInfo[0])
        opt = vtk.vtkPolyData.GetData(outInfo.GetInformationObject(0))

        if inp.GetNumberOfPoints() == 0:
            return

        new_points = vtk.vtkPoints()

        new_points.SetNumberOfPoints(2*inp.GetNumberOfPoints())

        j = 0

        for i in xrange(inp.GetNumberOfPoints()):
            point = inp.GetPoint(i)
            self.renderer.SetWorldPoint(point[0], point[1], point[2], 1)
            self.renderer.WorldToDisplay()
            dp = self.renderer.GetDisplayPoint()
            self.renderer.SetDisplayPoint(dp[0], dp[1], 0)
            self.renderer.DisplayToWorld()
            wp = self.renderer.GetWorldPoint()
            new_points.SetPoint(j, wp[:3])
            j += 1

        for i in xrange(inp.GetNumberOfPoints()):
            point = inp.GetPoint(i)
            self.renderer.SetWorldPoint(point[0], point[1], point[2], 1)
            self.renderer.WorldToDisplay()
            dp = self.renderer.GetDisplayPoint()
            self.renderer.SetDisplayPoint(dp[0], dp[1], 1)
            self.renderer.DisplayToWorld()
            wp = self.renderer.GetWorldPoint()
            new_points.SetPoint(j, wp[:3])
            j += 1

        new_data = vtk.vtkPolyData()

        cell_array = vtk.vtkCellArray()

        number_of_points = inp.GetNumberOfPoints()

        for i in xrange(inp.GetNumberOfCells()):
            cell = inp.GetCell(i)
            new_cell = vtk.vtkTriangle()
            new_cell.DeepCopy(cell)
            cell_array.InsertNextCell(new_cell)

        for i in xrange(inp.GetNumberOfCells()):
            cell = inp.GetCell(i)
            ids1 = cell.GetPointIds()
            new_cell = vtk.vtkTriangle()
            ids = new_cell.GetPointIds()
            ids.SetId(0, ids1.GetId(0) + number_of_points)
            ids.SetId(1, ids1.GetId(1) + number_of_points)
            ids.SetId(2, ids1.GetId(2) + number_of_points)
            cell_array.InsertNextCell(new_cell)

        for i in xrange(number_of_points):
            new_cell = vtk.vtkLine()
            ids = new_cell.GetPointIds()
            ids.SetId(0, i)
            ids.SetId(1, i + number_of_points)
            cell_array.InsertNextCell(new_cell)

        new_data.SetPoints(new_points)
        new_data.SetPolys(cell_array)
        new_data.SetLines(cell_array)

        opt.ShallowCopy(new_data)

        return 1


class PolyPicker(object):
    def __init__(self, model_picker):
        super(PolyPicker, self).__init__()

        self.model_picker = model_picker

        self.poly_picker = PolyPickFilter()
        self.poly_picker.set_renderer(self.model_picker.get_renderer())

        self._start_position = [0, 0]
        self._end_position = [0, 0]
        self._pixel_array = vtk.vtkUnsignedCharArray()

        self._left_button_down = False
        self._ctrl_left_button_down = False
        self._right_button_down = False
        self._middle_button_down = False

        self._down_pos = None
        self._up_pos = None

        self.polygon = vtk.vtkPolygon()

        self._point_list = []

        self.poly_data = vtk.vtkPolyData()
        self.poly_points = vtk.vtkPoints()
        self.poly_data.SetPoints(self.poly_points)

        self.cell_array = vtk.vtkCellArray()
        self.cell_array.InsertNextCell(self.polygon)
        self.cell_array.Squeeze()

        self.poly_data.SetPolys(self.cell_array)

        self.coordinate = vtk.vtkCoordinate()
        self.coordinate.SetCoordinateSystem(5)

        self.polygon_mapper = vtk.vtkPolyDataMapper()
        self.polygon_mapper.SetInputData(self.poly_data)

        self.polygon_actor = vtk.vtkActor()
        self.polygon_actor.SetMapper(self.polygon_mapper)
        self.polygon_actor.GetProperty().SetColor(0.5, 0.5, 0)
        self.polygon_actor.GetProperty().SetLineWidth(1)
        self.polygon_actor.GetProperty().SetRepresentationToWireframe()

        self.renderer = None
        self.add_renderer(self.model_picker.get_renderer_hovered())

        self.reset_polygon()

        self.tri_filter = vtk.vtkTriangleFilter()

        self.ex = vtk.vtkExtractSelection()
        self.selection_node = vtk.vtkSelectionNode()
        self.selection_node.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)
        self.ex_selection = vtk.vtkSelection()
        self.ex_selection.AddNode(self.selection_node)

        self.ex.SetInputConnection(0, self.poly_picker.GetOutputPort())
        self.ex.SetInputData(1, self.ex_selection)

        self._down_pos = None
        self._up_pos = None

        self._points = 0

        self.selection = None
        self.reset_selection()

        self.set_data()

        #self.helper = HelperFilter()
        #self.helper.set_renderer(self.renderer)

    def add_renderer(self, renderer):
        if self.renderer is not None:
            self.remove_renderer()

        self.renderer = renderer
        self.renderer.AddActor(self.polygon_actor)
        self.model_picker.render()

    def remove_renderer(self):
        self.renderer.RemoveActor(self.polygon_actor)
        self.renderer = None

    def reset_selection(self):
        self.selection = {'Node': [],
                          'Element': [],
                          'MPC': [],
                          'Load': [],
                          'Disp': []}

    def set_data(self):
        data = self.model_picker.visible_filter.all_data()
        self.poly_picker.SetInputDataObject(0, data)

    def reset_box_and_picked_data(self):
        self.reset_polygon()
        self.model_picker.reset_picked_data()

    def reset_polygon(self):
        self.poly_points.Reset()

        self.polygon = vtk.vtkPolygon()

        self.poly_data.SetPoints(self.poly_points)

        self.cell_array.Reset()
        self.cell_array.InsertNextCell(self.polygon)
        self.cell_array.Squeeze()

        self.poly_data.SetPolys(self.cell_array)

        self.polygon_mapper.SetInputData(self.poly_data)

        self.polygon_mapper.Modified()

    def begin_picking(self, interactor):

        pos = interactor.GetEventPosition()

        self._point_list = [pos]

        self._first_point = pos
        self._last_point = pos

        first_point = display_to_world(pos, self.model_picker.get_renderer(), .001)

        self.reset_polygon()

        self.poly_points.InsertNextPoint(first_point[:3])
        self.poly_points.InsertNextPoint(first_point[0] + .001, first_point[1] + .001, first_point[2] + .001)

        self.polygon.GetPointIds().InsertNextId(0)

        self._points = 1

        self.polygon.GetPointIds().InsertNextId(1)

        self.polygon.Modified()

    def self_intersecting(self):

        def on_segment(p, r, q):

            max0 = max(p[0], r[0])
            min0 = min(p[0], r[0])

            max1 = max(p[1], r[1])
            min1 = min(p[1], r[1])

            if min0 <= q[0] <= max0 and min1 <= q[1] <= max1:
                return True
            else:
                return False

        def orientation(p, r, q):
            val = int((q[1] - p[1])*(r[0] - q[0]) - (q[0] - p[0])*(r[1] - q[1]))

            if val == 0:
                return 0

            if val > 0:
                return 1
            else:
                return 2

        def does_intersect(p1, q1, p2, q2):

            if p1 == p2 or p1 == q2 or q1 == p2 or q1 == q2:
                return False

            o1 = orientation(p1, q1, p2)
            o2 = orientation(p1, q1, q2)
            o3 = orientation(p2, q2, p1)
            o4 = orientation(p2, q2, q1)

            if o1 != o2 and o3 != o4:
                return True

            if o1 == 0 and on_segment(p1, q1, p2):
                return True

            if o2 == 0 and on_segment(p1, q1, q2):
                return True

            if o3 == 0 and on_segment(p2, q2, p1):
                return True

            if o4 == 0 and on_segment(p2, q2, q1):
                return True

            return False

        pl = self._point_list

        points = len(pl)

        if points <= 2:
            return False

        e1 = [pl[0], pl[points-1]]
        e2 = [pl[points-2], pl[points-1]]

        for i in xrange(1, points-1):
            p1 = pl[i]
            p2 = pl[i-1]

            if does_intersect(p1, p2, e1[0], e1[1]) or does_intersect(p1, p2, e2[0], e2[1]):
                return True

        return False

    def add_point(self, interactor):

        def distance(p1, p2):
            sum = (p1[0] - p2[0])**2
            sum += (p1[1] - p2[1])**2

            return sum ** 0.5

        pos = interactor.GetEventPosition()

        if self._points > 2 and (distance(pos, self._last_point) < 5 or distance(pos, self._first_point) < 5):
            self.end_picking(interactor)
            return True

        next_point = display_to_world(pos, self.model_picker.get_renderer(), .001)

        self.poly_points.SetPoint(self._points, next_point[:3])

        self._point_list.append(pos)

        if self.self_intersecting():
            self._point_list.pop()
            return False

        self._last_point = pos

        self.poly_points.InsertNextPoint(next_point[0] + .001, next_point[1] + .001, next_point[2] + .001)

        self._points += 1

        self.polygon.GetPointIds().InsertNextId(self._points)

        self.polygon.Modified()

        return False

    def mouse_move(self, interactor):

        pos = interactor.GetEventPosition()
        next_point = display_to_world(pos, self.model_picker.get_renderer(), .001)

        self.poly_points.SetPoint(self._points, next_point[:3])
        self.poly_points.Modified()

        self.polygon.Modified()

        self.poly_data.SetPoints(self.poly_points)

        self.cell_array.Reset()
        self.cell_array.InsertNextCell(self.polygon)
        self.cell_array.Squeeze()

        self.poly_data.SetPolys(self.cell_array)
        self.poly_data.Modified()

        self.polygon_mapper.SetInputData(self.poly_data)
        self.polygon_mapper.Modified()

        self.model_picker.render()

    def end_picking(self, interactor):

        self.poly_picker.set_poly_pick_data(self.poly_data)
        self.poly_picker.Modified()

        #triangles = vtk.vtkTriangleFilter()
        #triangles.SetInputData(self.poly_data)
        #triangles.Modified()
        #triangles.Update()

        #self.helper.SetInputDataObject(0, triangles.GetOutput())
        #self.helper.Modified()
        #self.helper.Update()

        #self.polygon_mapper.SetInputData(self.helper.GetOutputDataObject(0))
        #self.polygon_mapper.Modified()

        self.something_picked()

    def something_picked(self):

        self.selection_node.SetSelectionList(self.model_picker.active_selections.selection_threshold())
        self.selection_node.Modified()
        self.ex_selection.Modified()

        self.ex.Update()

        data = self.ex.GetOutput()

        self.reset_polygon()

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