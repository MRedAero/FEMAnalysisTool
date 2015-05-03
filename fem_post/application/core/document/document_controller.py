__author__ = 'Michael Redmond'

import gc

from base_app.simple_pubsub import pub

from base_app.application.core.document import BaseAppDocumentController

from document import FemAnalysisToolDocument


class FemAnalysisToolDocumentController(BaseAppDocumentController):
    def __init__(self, view_controller):
        super(FemAnalysisToolDocumentController, self).__init__(view_controller)

        self._view_controller = self._view_controller
        """:type: fem_post.application.core.view.view_controller.FemAnalysisToolViewController"""

        self._view = self._view_controller.get_view()

        self._active_document = self._active_document
        """:type: FemAnalysisToolDocument"""

        self._documents = self._documents
        """:type: list [FemAnalysisToolDocument]"""

    def _subscribe_to_pub(self):
        super(FemAnalysisToolDocumentController, self)._subscribe_to_pub()
        pub.subscribe(self._show_hide, 'vtk.show_hide')
        pub.subscribe(self._switch_view, 'vtk.switch_view')

    def get_active_vtk(self):
        return self._active_document.get_vtk_widget()

    def _create_document(self, document_name, mdi_controller):
        return FemAnalysisToolDocument(document_name, mdi_controller)

    def _show_hide(self):
        self._active_document.get_vtk_widget().show_hide_selection()

    def _switch_view(self):
        self._active_document.get_vtk_widget().switch_view()

