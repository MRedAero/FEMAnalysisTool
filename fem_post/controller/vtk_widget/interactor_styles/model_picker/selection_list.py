__author__ = 'Michael Redmond'

from PySide import QtCore
import vtk

from controller.vtk_widget.vtk_globals import vtk_globals

import re

delimiters = " ", ",", ";", "\t"
regex_pattern = '|'.join(map(re.escape, delimiters))


class SelectionList(QtCore.QObject):

    selection_changed = QtCore.Signal()

    def __init__(self):
        super(SelectionList, self).__init__()

        self.nodes = []
        self.elements = []
        self.mpcs = []
        self.loads =[]
        self.disps = []

        self.selection_type = vtk_globals.SELECTION_REPLACE

    def update_selection(self, selections):
        if self.selection_type == vtk_globals.SELECTION_REPLACE:
            self._replace_selection(selections)
        elif self.selection_type == vtk_globals.SELECTION_APPEND:
            self._append_selection(selections)
        elif self.selection_type == vtk_globals.SELECTION_REMOVE:
            self._remove_selection(selections)

    def reset(self):
        self.nodes = []
        self.elements = []
        self.mpcs = []
        self.loads =[]
        self.disps = []

        self.selection_changed.emit()

    def all_selection(self):
        return self.nodes + self.elements + self.mpcs + self.loads + self.disps

    def all_selection_vtk_array(self):

        vtk_array = vtk.vtkIntArray()

        selection_list = self.all_selection()

        vtk_array.SetNumberOfTuples(len(selection_list))

        my_int = int

        # TODO: speed this up using numpy?
        for i in xrange(len(selection_list)):
            vtk_array.SetValue(i, my_int(selection_list[i]))

        return vtk_array

    def _replace_selection(self, selections):
        try:
            self.nodes = self.expand_selection(selections['Node'])
        except KeyError:
            self.nodes = []

        try:
            self.elements = self.expand_selection(selections['Element'])
        except KeyError:
            self.elements = []

        try:
            self.mpcs = self.expand_selection(selections['MPC'])
        except KeyError:
            self.mpcs = []

        try:
            self.loads = self.expand_selection(selections['Load'])
        except KeyError:
            self.loads = []

        try:
            self.disps = self.expand_selection(selections['Disp'])
        except KeyError:
            self.disps = []

        self.selection_changed.emit()

    def _append_selection(self, selections):
        try:
            new_list = self.expand_selection(selections['Node'])
            self.nodes = self.nodes + list(set(new_list) - set(self.nodes))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['Element'])
            self.elements = self.elements + list(set(new_list) - set(self.elements))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['MPC'])
            self.mpcs = self.mpcs + list(set(new_list) - set(self.mpcs))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['Load'])
            self.loads = self.loads + list(set(new_list) - set(self.loads))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['Disp'])
            self.disps = self.disps + list(set(new_list) - set(self.disps))
        except KeyError:
            pass

        self.selection_changed.emit()

    def _remove_selection(self, selections):
        try:
            new_list = self.expand_selection(selections['Node'])
            self.nodes = list(set(self.nodes) - set(new_list))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['Element'])
            self.elements = list(set(self.elements) - set(new_list))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['MPC'])
            self.mpcs = list(set(self.mpcs) - set(new_list))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['Load'])
            self.loads = list(set(self.loads) - set(new_list))
        except KeyError:
            pass

        try:
            new_list = self.expand_selection(selections['Disp'])
            self.disps = list(set(self.disps) - set(new_list))
        except KeyError:
            pass

        self.selection_changed.emit()

    def expand_selection(self, selection):

        if isinstance(selection, list) and len(selection) == 0:
            return []

        if not isinstance(selection, list):
            selection_list = re.split(regex_pattern, str(selection))
        else:
            selection_list = selection

        expanded_selection = []

        # TODO: speed this up using numpy?
        for i in xrange(len(selection_list)):

            if isinstance(selection_list[i], int):
                expanded_selection.append(selection_list[i])
                continue

            tmp = selection_list[i].split(':')

            offset = 1

            if len(tmp) == 1:
                expanded_selection.append(tmp[0])
                continue
            if len(tmp) >= 2:
                begin = tmp[0]
                end = tmp[1]
            if len(tmp) == 3:
                offset = tmp[2]

            for j in xrange(begin, end + offset, offset):
                expanded_selection.append(j)

        return expanded_selection

    def condense_selection(self, selection):
        pass

    def to_string(self):
        result = ''

        global_id = vtk_globals.global_id

        my_str = str

        if len(self.nodes) > 0:
            nodes = map(global_id, self.nodes)
            nodes = map(my_str, nodes)
            result += 'Node ' + ' '.join(nodes)

        if len(self.elements) > 0:
            elements = map(global_id, self.elements)
            elements = map(my_str, elements)
            result += ' Element ' + ' '.join(elements)

        if len(self.mpcs) > 0:
            mpcs = map(global_id, self.mpcs)
            mpcs = map(my_str, mpcs)
            result += ' MPC ' + ' '.join(mpcs)

        return result
