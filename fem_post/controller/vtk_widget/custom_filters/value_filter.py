__author__ = 'Michael Redmond'

import vtk


class ValueFilter(vtk.vtkProgrammableFilter):
    def __init__(self, value_selection):
        self.SetExecuteMethod(self.execute)

        self.s_sel = vtk.vtkSelection()
        self.s_unsel = vtk.vtkSelection()

        self.n_sel = vtk.vtkSelectionNode()
        self.n_unsel = vtk.vtkSelectionNode()

        self.ex_sel = vtk.vtkExtractSelection()
        self.ex_unsel = vtk.vtkExtractSelection()

        self.n_sel.SetContentType(vtk.vtkSelectionNode.VALUES)
        self.n_unsel.SetContentType(vtk.vtkSelectionNode.VALUES)

        self.n_unsel.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)

        self.value_selection = None
        self.set_value_selection(value_selection, True)

        self.s_sel.AddNode(self.n_sel)
        self.s_unsel.AddNode(self.n_unsel)

        self.ex_sel.SetInputData(1, self.s_sel)
        self.ex_unsel.SetInputData(1, self.s_unsel)

    def set_input_data(self, input_data, do_not_execute=False):

        self.SetInputData(input_data)

        self.ex_sel.SetInputData(0, input_data)
        self.ex_unsel.SetInputData(0, input_data)

        self.ex_sel.Update()
        self.ex_unsel.Update()

        if not do_not_execute:
            self.execute()

    def set_value_selection(self, value_selection, do_not_execute=False):
        self.value_selection = value_selection

        self.n_sel.SetSelectionList(self.value_selection)
        self.n_unsel.SetSelectionList(self.value_selection)

        if not do_not_execute:
            self.execute()

    def selected_data(self):
        return self.ex_sel.GetOutput()

    def unselected_data(self):
        return self.ex_unsel.GetOutput()

    def execute(self):
        self.n_sel.Modified()
        self.n_unsel.Modified()
