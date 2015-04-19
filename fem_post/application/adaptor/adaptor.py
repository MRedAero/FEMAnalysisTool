__author__ = 'Michael Redmond'

from base_app.application.adaptor import BaseAppAdaptor

from fem_post.application.controller.model import FemAnalysisToolModelController
from fem_post.application.controller.view import FemAnalysisToolViewController
from fem_post.application.controller.logic import FemAnalysisToolLogicController
from fem_post.application.controller.core_plugins import FemAnalysisToolCorePlugins


class FemAnalysisToolAdaptor(BaseAppAdaptor):
    def __init__(self, app):
        super(FemAnalysisToolAdaptor, self).__init__(app)

        self._core_plugins_controller = FemAnalysisToolCorePlugins(self)

    @property
    def create_model_controller_object(self):
        return FemAnalysisToolModelController

    @property
    def create_view_controller_object(self):
        return FemAnalysisToolViewController

    @property
    def create_logic_controller_object(self):
        return FemAnalysisToolLogicController

    def show_hide(self):
        self._view_controller.show_hide()

    def switch_view(self):
        self._view_controller.switch_view()

    def get_central_widget(self):
        return self._view_controller.get_central_widget()

    def add_dock_widget(self, dock_area, dock_widget):
        self._view_controller.add_dock_widget(dock_area, dock_widget)
