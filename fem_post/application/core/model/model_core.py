__author__ = 'Michael Redmond'


from base_app.application.core.model.model_core import BaseAppModelCore


class FemAnalysisToolModelCore(BaseAppModelCore):
    def __init__(self, name):
        super(FemAnalysisToolModelCore, self).__init__(name)

        self._file = self._file
        """:type: tables.File"""