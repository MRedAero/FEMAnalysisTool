__author__ = 'Michael Redmond'

import vtk

from ..vtk_globals import VTK_VERSION


class GlobalIdFilter(vtk.vtkProgrammableFilter):
    def __init__(self):
        self.SetExecuteMethod(self.execute)

        self.s_sel = vtk.vtkSelection()
        self.s_unsel = vtk.vtkSelection()

        self.n_sel = vtk.vtkSelectionNode()
        self.n_unsel = vtk.vtkSelectionNode()

        self.ex_sel = vtk.vtkExtractSelection()
        self.ex_unsel = vtk.vtkExtractSelection()

        self.n_sel.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)
        self.n_unsel.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)

        self.n_unsel.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)

        self.global_id_selection = None

        self.s_sel.AddNode(self.n_sel)
        self.s_unsel.AddNode(self.n_unsel)

        if VTK_VERSION >= 6.0:
            self.ex_sel.SetInputData(1, self.s_sel)
            self.ex_unsel.SetInputData(1, self.s_unsel)
        else:
            self.ex_sel.SetInput(1, self.s_sel)
            self.ex_unsel.SetInput(1, self.s_unsel)

    def set_input_data(self, input_data, do_not_execute=False):

        if VTK_VERSION >= 6.0:

            self.SetInputData(input_data)

            self.ex_sel.SetInputData(0, input_data)
            self.ex_unsel.SetInputData(0, input_data)
        else:
            self.SetInput(input_data)

            self.ex_sel.SetInput(0, input_data)
            self.ex_unsel.SetInput(0, input_data)

        self.ex_sel.Update()
        self.ex_unsel.Update()

        if not do_not_execute:
            self.execute()

    def set_global_id_selection(self, global_id_selection, do_not_execute=False):

        if isinstance(global_id_selection, list):
            int_array = vtk.vtkIntArray()
            for i in xrange(len(global_id_selection)):
                int_array.InsertNextValue(int(global_id_selection[i]))

            self.global_id_selection = int_array

        else:
            self.global_id_selection = global_id_selection

        self.n_sel.SetSelectionList(self.global_id_selection)
        self.n_unsel.SetSelectionList(self.global_id_selection)

        if not do_not_execute:
            self.execute()

    def selected_data(self):
        return self.ex_sel.GetOutput()

    def unselected_data(self):
        return self.ex_unsel.GetOutput()

    def execute(self):
        self.n_sel.Modified()
        self.n_unsel.Modified()
