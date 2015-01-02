__author__ = 'Michael Redmond'

import vtk

from .extract_selection_filter import ExtractSelectionFilter


class GlobalIdFilter(ExtractSelectionFilter):
    def __init__(self):
        ExtractSelectionFilter.__init__(self, None)

        self.n_sel.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)
        self.n_unsel.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)

    def set_selection_list(self, selection_list, do_not_execute=False):

        if isinstance(selection_list, list):
            int_array = vtk.vtkIntArray()
            for i in xrange(len(selection_list)):
                int_array.InsertNextValue(int(selection_list[i]))

            self.selection_list = int_array

        else:
            self.selection_list = selection_list

        self.n_sel.SetSelectionList(self.selection_list)
        self.n_unsel.SetSelectionList(self.selection_list)

        if not do_not_execute:
            self.execute()
