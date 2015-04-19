__author__ = 'Michael Redmond'

from fem_post.application.core.plugins.vtk_selections_test import VTKSelectionsTestAdaptor


class FemAnalysisToolCorePlugins(object):
    def __init__(self, adaptor):
        super(FemAnalysisToolCorePlugins, self).__init__()

        self._adaptor = adaptor
        """:type: fem_post.application.adaptor.FEMAnalysisToolAdaptor"""

        self._vtk_selections_test = VTKSelectionsTestAdaptor(self._adaptor)