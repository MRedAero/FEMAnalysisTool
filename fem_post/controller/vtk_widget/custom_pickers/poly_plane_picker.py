__author__ = 'Michael Redmond'

import vtk


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

        self.extractor.SetInputData(self.input_data)

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

        self.hover_data = vtk.vtkUnstructuredGrid()
        self.selected_data = vtk.vtkUnstructuredGrid()

        self.hover_mapper = vtk.vtkDataSetMapper()
        self.selected_mapper = vtk.vtkDataSetMapper()

        self.hover_mapper.SetInputData(self.hover_data)
        self.selected_mapper.SetInputData(self.selected_data)

        self.hover_actor = vtk.vtkActor()
        self.selected_actor = vtk.vtkActor()

        self.hover_actor.SetMapper(self.hover_mapper)
        self.selected_actor.SetMapper(self.selected_mapper)

    def set_pipeline(self, pipeline):
        if self.pipeline is not None:
            self.pipeline.data_updated.disconnect(self.update_data)

        self.pipeline = pipeline
        """:type: fem_post.controller.vtk_widget.pipelines.DataPipeline"""

        self.pipeline.data_updated.connect(self.update_data)

        self.update_data()

    def update_data(self):
        if self.pipeline is None:
            return

        self.node_extractor.set_input_data(self.pipeline.node_mapper.GetInput())
        self.element_extractor.set_input_data(self.pipeline.element_mapper.GetInput())
        self.rbe_extractor.set_input_data(self.pipeline.rbe_mapper.GetInput())

    def reset(self):
        self.poly_points.Reset()
        self.poly_line.Reset()

        self.hover_data.Reset()
        self.selected_data.Reset()