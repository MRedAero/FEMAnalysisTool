__author__ = 'Michael Redmond'

import vtk
from PySide import QtCore

from ..vtk_globals import VTK_VERSION


class DataPipeline(QtCore.QObject):

    data_updated = QtCore.Signal()

    def __init__(self, data, renderer):
        super(DataPipeline, self).__init__()

        self._data = data
        self._renderer = renderer

        self.node_mapper = vtk.vtkDataSetMapper()
        self.element_mapper = vtk.vtkDataSetMapper()
        self.rbe_mapper = vtk.vtkDataSetMapper()

        self.node_actor = vtk.vtkActor()
        self.element_actor = vtk.vtkActor()
        self.rbe_actor = vtk.vtkActor()

        self.element_actor.GetProperty().SetOpacity(0.5)

        self.node_actor.SetMapper(self.node_mapper)
        self.element_actor.SetMapper(self.element_mapper)
        self.rbe_actor.SetMapper(self.rbe_mapper)

        self._renderer.AddActor(self.node_actor)
        self._renderer.AddActor(self.element_actor)
        self._renderer.AddActor(self.rbe_actor)

        self.shown = False
        self.toggle_shown()

        self.update()

    def set_data(self, data):
        self._data = data
        self.update()

    def get_data(self):
        return self._data

    def set_renderer(self, renderer):
        self._renderer = renderer
        self.update()

    def get_renderer(self):
        return self._renderer

    def update(self):
        self._data.update()

        self.node_mapper.Modified()
        self.element_mapper.Modified()
        self.rbe_mapper.Modified()

        self.data_updated.emit()

    def toggle_shown(self):
        if VTK_VERSION >= 6.0:
            if self.shown:
                self.shown = False
                self.node_mapper.SetInputData(self._data.hidden_nodes())
                self.element_mapper.SetInputData(self._data.hidden_elements())
                self.rbe_mapper.SetInputData(self._data.hidden_rbes())
            else:
                self.shown = True
                self.node_mapper.SetInputData(self._data.shown_nodes())
                self.element_mapper.SetInputData(self._data.shown_elements())
                self.rbe_mapper.SetInputData(self._data.shown_rbes())
        else:
            if self.shown:
                self.shown = False
                self.node_mapper.SetInput(self._data.hidden_nodes())
                self.element_mapper.SetInput(self._data.hidden_elements())
                self.rbe_mapper.SetInput(self._data.hidden_rbes())
            else:
                self.shown = True
                self.node_mapper.SetInput(self._data.shown_nodes())
                self.element_mapper.SetInput(self._data.shown_elements())
                self.rbe_mapper.SetInput(self._data.shown_rbes())

        self.data_updated.emit()