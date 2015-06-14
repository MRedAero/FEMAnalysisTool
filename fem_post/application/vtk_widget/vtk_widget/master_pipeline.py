__author__ = 'Michael Redmond'

import vtk

from fem_post.application.vtk_widget.pipelines.base_pipeline import BasePipeline

from fem_post.application.vtk_widget.algorithms import (BDFDataSource, VisibleFilter, GroupFilter, GlobalIdFilter)
from .new_split_data_filter import SplitDataFilter

import vtk_pub


def get_current_selection():
    return None


class MasterPipeline(object):
    def __init__(self, vtk_widget):
        """
        Contains all 3 pipelines and associated logic.
        :type vtk_widget: fem_post.application.vtk_widget.VTKWidget
        :return:
        """
        self._vtk_widget = vtk_widget

        self._renderer, self._renderer_picked, self._renderer_hovered = self._vtk_widget.get_renderers()

        self.data_source = BDFDataSource()
        self.group_selections_poly_data = vtk.vtkPolyData()
        self.group_selections = self.group_selections_poly_data.GetCellData()
        # this is temporary for now until grouping features are added
        self.group_selections.AddArray(self.data_source.default_group)

        self.group_filter = GroupFilter()
        self.group_filter.SetInputConnection(0, self.data_source.GetOutputPort(0))
        self.group_filter.set_group_selections(self.group_selections)

        self.visible_filter = VisibleFilter()
        self.visible_filter.SetInputConnection(0, self.group_filter.GetOutputPort(0))

        filter_ = SplitDataFilter()
        filter_.SetInputConnection(self.visible_filter.all_port())
        self.main_pipeline = BasePipeline(self._renderer, filter_)

        filter_ = GlobalIdFilter()
        filter_.SetInputConnection(self.visible_filter.all_port())
        self.selected_global_id_filter = filter_
        filter_ = SplitDataFilter()
        filter_.SetInputConnection(self.selected_global_id_filter.GetOutputPort(0))
        self.selected_pipeline = BasePipeline(self._renderer_picked, filter_)

        filter_ = GlobalIdFilter()
        filter_.SetInputConnection(self.visible_filter.all_port())
        self.hovered_global_id_filter = filter_
        filter_ = SplitDataFilter()
        filter_.SetInputConnection(self.selected_global_id_filter.GetOutputPort(0))
        self.hovered_pipeline = BasePipeline(self._renderer_hovered, filter_)

        self.toggle_filter = vtk.vtkExtractSelection()
        self.toggle_filter.SetInputConnection(0, self.visible_filter.all_port())

        self.toggle_selection_node = vtk.vtkSelectionNode()
        self.toggle_selection_node.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)
        self.toggle_selection = vtk.vtkSelection()
        self.toggle_selection.AddNode(self.toggle_selection_node)

        self.toggle_filter.SetInputData(1, self.toggle_selection)

        self._subscribe_to_pub()

    def _subscribe_to_pub(self):
        self._vtk_widget.get_pub().subscribe(self.switch_view, vtk_pub.subscribe.switch_view())
        self._vtk_widget.get_pub().subscribe(self.show_hide, vtk_pub.subscribe.show_hide())

    def set_file(self, file):
        self.data_source.set_file(file)
        self.data_source.Update()
        vtk_pub.publish.fit_view()

    def switch_view(self):
        """
        Switches the view from shown to hidden and vice versa.
        :return:
        """
        self.visible_filter.toggle_visible()
        self._vtk_widget.render()

    def show_hide(self):
        """
        Toggles current selection between shown and hidden.
        :return:
        """

        current_selection = get_current_selection()
        self.toggle_selection_node.SetSelectionList(current_selection)
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
        self._vtk_widget.render()