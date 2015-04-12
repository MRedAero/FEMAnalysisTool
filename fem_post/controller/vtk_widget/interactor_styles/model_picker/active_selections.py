__author__ = 'Michael Redmond'

from PyQt4 import QtCore
import vtk

from fem_post.controller.vtk_widget.vtk_globals import vtk_globals


class ActiveSelections(QtCore.QObject):
    """This is a helper class for ModelPicker"""

    selection_changed = QtCore.Signal()

    def __init__(self):
        super(ActiveSelections, self).__init__()

        self._skip = 0

        self._any = True

        self._nodes = True
        self._elements = True
        self._mpcs = True

        self._points = True
        self._bars = True
        self._tris = True
        self._quads = True

    def selection_threshold(self):
        selection_threshold = vtk.vtkIntArray()
        selection_threshold.SetName("basic_shapes")

        selection_threshold.SetNumberOfComponents(1)

        if self._nodes:
            selection_threshold.InsertNextValue(vtk_globals.VTK_NODE)
            selection_threshold.InsertNextValue(vtk_globals.VTK_NODE)

        if self._points:
            selection_threshold.InsertNextValue(vtk_globals.VTK_VERTEX)
            selection_threshold.InsertNextValue(vtk_globals.VTK_VERTEX)

        if self._bars:
            selection_threshold.InsertNextValue(vtk_globals.VTK_LINE)
            selection_threshold.InsertNextValue(vtk_globals.VTK_LINE)

        if self._tris:
            selection_threshold.InsertNextValue(vtk_globals.VTK_TRI)
            selection_threshold.InsertNextValue(vtk_globals.VTK_TRI)

        if self._quads:
            selection_threshold.InsertNextValue(vtk_globals.VTK_QUAD)
            selection_threshold.InsertNextValue(vtk_globals.VTK_QUAD)

        if self._mpcs:
            selection_threshold.InsertNextValue(vtk_globals.VTK_POLY_LINE)
            selection_threshold.InsertNextValue(vtk_globals.VTK_POLY_LINE)

        return selection_threshold

    def selection_changed_emit(self):
        if self._skip:
            self._skip -= 1
            return

        self.selection_changed.emit()

    @property
    def any(self):
        return self._any

    @any.setter
    def any(self, value):

        self._any = value

        self._nodes = value
        self._elements = value

        self._points = value
        self._bars = value
        self._tris = value
        self._quads = value

        self._mpcs = value

        self.selection_changed_emit()

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

        self.selection_changed_emit()

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        self._elements = value

        self._points = value
        self._bars = value
        self._tris = value
        self._quads = value

        self.selection_changed_emit()

    @property
    def mpcs(self):
        return self._mpcs

    @mpcs.setter
    def mpcs(self, value):
        self._mpcs = value

        self.selection_changed_emit()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

        self.selection_changed_emit()

    @property
    def bars(self):
        return self._bars

    @bars.setter
    def bars(self, value):
        self._bars = value

        self.selection_changed_emit()

    @property
    def tris(self):
        return self._tris

    @tris.setter
    def tris(self, value):
        self._tris = value

        self.selection_changed_emit()

    @property
    def quads(self):
        return self._quads

    @quads.setter
    def quads(self, value):
        self._quads = value

        self.selection_changed_emit()

    def toggle_picking(self, entity_type, index):
        if entity_type == 0:
            self.any = not self.any
            return
        elif entity_type == 1:
            self.nodes = not self.nodes
            return
        elif entity_type == 2 and index is None:
            self.elements = not self.elements
            return

        if index == 1:
            self.points = not self.points
        elif index == 2:
            self.bars = not self.bars
        elif index == 3:
            self.tris = not self.tris
        elif index == 4:
            self.quads = not self.quads