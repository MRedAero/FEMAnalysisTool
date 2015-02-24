__author__ = 'Michael Redmond'

from PySide import QtCore

from ...vtk_globals import vtk_globals

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

        self.selection_type = SELECTION_REPLACE

    def update_selection(self, selections):
        if self.selection_type == SELECTION_REPLACE:
            self._replace_selection(selections)
        elif self.selection_type == SELECTION_APPEND:
            self._append_selection(selections)
        elif self.selection_type == SELECTION_REMOVE:
            self._remove_selection(selections)

    def reset(self):
        self.nodes = []
        self.elements = []
        self.mpcs = []
        self.loads =[]
        self.disps = []

        self.selection_changed.emit()

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

        for i in xrange(len(selection_list)):
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

        if len(self.nodes) > 0:
            result += 'Node ' + ' '.join(self.nodes)

        if len(self.elements) > 0:
            result += ' Element ' + ' '.join(self.elements)

        if len(self.mpcs) > 0:
            result += ' MPC ' + ' '.join(self.mpcs)

        return result
