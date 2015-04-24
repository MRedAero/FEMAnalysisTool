__author__ = 'Michael Redmond'

from base_app.application.core.model import BaseAppModelController

from model_core import FemAnalysisToolModelCore


class FemAnalysisToolModelController(BaseAppModelController):
    def __init__(self):
        super(FemAnalysisToolModelController, self).__init__()

        self._models = self._models
        """:type: list [FemAnalysisToolModelCore]"""

        self._active_model = self._active_model
        """:type: FemAnalysisToolModelCore"""

    @property
    def create_model_core_object(self):
        return FemAnalysisToolModelCore