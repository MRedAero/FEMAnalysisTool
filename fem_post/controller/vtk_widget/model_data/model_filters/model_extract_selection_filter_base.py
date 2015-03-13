import vtk


class ModelExtractSelectionFilterBase(vtk.vtkProgrammableFilter):
    def __init__(self, selected=None):
        self.SetExecuteMethod(self.execute)

        self.s_sel = vtk.vtkSelection()
        self.n_sel = vtk.vtkSelectionNode()
        self.ex_sel = vtk.vtkExtractSelection()

        self.n_sel.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)

        self.selection_list = None
        self.selection_list_type = None
        self.selection_list_var_typ = None

        self.select_integers()

        self.selection_list = None

        if selected is not None:
            self.set_selection_list(selected, True)

        self.s_sel.AddNode(self.n_sel)
        self.ex_sel.SetInputData(1, self.s_sel)

        self.input_filter = None

    def filter_thresholds(self):
        self.n_sel.SetContentType(vtk.vtkSelectionNode.THRESHOLDS)

    def filter_ids(self):
        self.n_sel.SetContentType(vtk.vtkSelectionNode.IDS)

    def filter_global_ids(self):
        self.n_sel.SetContentType(vtk.vtkSelectionNode.GLOBALIDS)

    # this is SLOW, use thresholds instead
    def filter_values(self):
        self.n_sel.SetContentType(vtk.vtkSelectionNode.VALUES)

    def set_input_data(self, input_data, do_not_execute=False):

        self.SetInputData(input_data)
        self.ex_sel.SetInputData(0, input_data)

        if not do_not_execute:
            self.Update()

    def set_input_connection(self, input_filter, do_not_execute=False):

        self.input_filter = input_filter

        self.SetInputConnection(input_filter.GetOutputPort())
        self.ex_sel.SetInputConnection(0, input_filter.GetOutputPort())

        if not do_not_execute:
            self.Update()

    def select_integers(self):
        self.set_selection_list_type = vtk.vtkIntArray
        self.selection_list_var_typ = int

    def select_floats(self):
        self.set_selection_list_type = vtk.vtkFloatArray
        self.selection_list_var_typ = float

    def set_selection_list(self, selection_list, do_not_execute=False):

        my_type = self.selection_list_var_typ

        if isinstance(selection_list, list):
            new_array = self.selection_list_type()
            new_array.SetNumberOfTuples(len(selection_list))

            for i in xrange(len(selection_list)):
                new_array.SetValue(i, my_type(selection_list[i]))

            self.selection_list = new_array

        else:
            self.selection_list = selection_list

        self.n_sel.SetSelectionList(self.selection_list)

        if not do_not_execute:
            self.Update()

    def reset(self):
        self.GetOutput().Reset()
        self.Modified()

    def selected_data(self):
        return self.ex_sel.GetOutput()

    def execute(self):

        if self.GetInput().GetNumberOfCells() == 0:
            self.GetOutput().Reset()
            return

        self.n_sel.Modified()
        self.ex_sel.Update()

        self.GetOutput().ShallowCopy(self.ex_sel.GetOutput())