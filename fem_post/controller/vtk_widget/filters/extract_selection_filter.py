__author__ = 'Michael Redmond'

import vtk

from ..vtk_globals import VTK_VERSION


class ExtractSelectionFilter(vtk.vtkProgrammableFilter):
    def __init__(self, selected):
        self.SetExecuteMethod(self.execute)

        self.s_sel = vtk.vtkSelection()
        self.s_unsel = vtk.vtkSelection()

        self.n_sel = vtk.vtkSelectionNode()
        self.n_unsel = vtk.vtkSelectionNode()

        self.ex_sel = vtk.vtkExtractSelection()
        self.ex_unsel = vtk.vtkExtractSelection()

        self.n_sel.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)
        self.n_unsel.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)

        self.n_unsel.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)

        self.selection_list = None
        self.set_selection_list(selected, True)

        self.s_sel.AddNode(self.n_sel)
        self.s_unsel.AddNode(self.n_unsel)

        if VTK_VERSION >= 6.0:
            self.ex_sel.SetInputData(1, self.s_sel)
            self.ex_unsel.SetInputData(1, self.s_unsel)
        else:
            self.ex_sel.SetInput(1, self.s_sel)
            self.ex_unsel.SetInput(1, self.s_unsel)

    def filter_thresholds(self):
        self.n_sel.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)
        self.n_unsel.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)

    # this is SLOW, use thresholds instead
    def filter_values(self):
        self.n_sel.SetContentType(vtk.vtkSelectionNode.VALUES)
        self.n_unsel.SetContentType(vtk.vtkSelectionNode.VALUES)

    def set_input_data(self, input_data, do_not_execute=False):

        if VTK_VERSION >= 6.0:
            self.SetInputData(input_data)

            self.ex_sel.SetInputData(0, input_data)
            self.ex_unsel.SetInputData(0, input_data)
        else:
            self.SetInput(input_data)

            self.ex_sel.SetInput(0, input_data)
            self.ex_unsel.SetInput(0, input_data)

        if not do_not_execute:
            self.execute()

    def set_selection_list(self, selected, do_not_execute=False):
        self.selection_list = selected

        self.n_sel.SetSelectionList(self.selection_list)
        self.n_unsel.SetSelectionList(self.selection_list)

        if not do_not_execute:
            self.execute()

    def selected_data(self):
        return self.ex_sel.GetOutput()

    def unselected_data(self):
        return self.ex_unsel.GetOutput()

    def execute(self):
        self.ex_sel.Update()
        self.ex_unsel.Update()
        self.n_sel.Modified()
        self.n_unsel.Modified()