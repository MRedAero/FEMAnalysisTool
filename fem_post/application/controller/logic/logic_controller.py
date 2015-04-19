__author__ = 'Michael Redmond'

from base_app.application.controller.logic import BaseAppLogicController

from fem_post.application.core.logic import logic_core


class FemAnalysisToolLogicController(BaseAppLogicController):
    def __init__(self, adaptor):
        super(FemAnalysisToolLogicController, self).__init__(adaptor)

        self._adaptor = self._adaptor
        """:type: fem_post.application.adaptor.FemAnalysisToolAdaptor"""

    def open_file(self, filename):
        return logic_core.open_file(filename)