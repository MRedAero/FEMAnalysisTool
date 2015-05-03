__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub

from base_app.application.core.document.document import BaseAppDocument

from fem_post.application.core.model import FemAnalysisToolModelCore
from fem_post.application.vtk_widget import VTKWidget



class FemAnalysisToolDocument(BaseAppDocument):
    def __init__(self, document_name, mdi_controller):
        super(FemAnalysisToolDocument, self).__init__(document_name, mdi_controller)

        self._vtk_widget = VTKWidget(self._subwindow)

    def get_vtk_widget(self):
        return self._vtk_widget

    def unload(self, index):
        self._vtk_widget.unload()
        super(FemAnalysisToolDocument, self).unload(index)

    def show_hide(self):
        self._vtk_widget.toggle_selected()

    def toggle_visible(self):
        self._vtk_widget.toggle_visible()

    def _create_model(self, document_name):
        return FemAnalysisToolModelCore(document_name)