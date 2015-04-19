__author__ = 'Michael Redmond'

from base_app.application.controller.model import BaseAppModelController

from fem_post.application.core.model import FemAnalysisToolModelCore


class FemAnalysisToolModelController(BaseAppModelController):
    def __init__(self, adaptor):
        super(FemAnalysisToolModelController, self).__init__(adaptor)

        self._adaptor = self._adaptor
        """:type: fem_post.application.adaptor.FemAnalysisToolAdaptor"""

        self._models = self._models
        """:type: list [FemAnalysisToolModelCore]"""

        self._active_model = self._active_model
        """:type: FemAnalysisToolModelCore"""

    @property
    def create_model_core_object(self):
        return FemAnalysisToolModelCore