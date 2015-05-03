__author__ = 'Michael Redmond'

# put this at the top of all files to check for license (where needed)
from base_app.license_manager import license_manager
license_manager.check_license()

from PyQt4 import QtGui, QtCore
QtCore.Signal = QtCore.pyqtSignal
import sys

from base_app.application import BaseApplication

from fem_post.application.core import FemAnalysisToolProgramController


class FEMAnalysisToolApplication(BaseApplication):
    def __init__(self):
        super(FEMAnalysisToolApplication, self).__init__()

    def create_program_controller_object(self, app):
        return FemAnalysisToolProgramController(app)


if __name__ == "__main__":
    app = FEMAnalysisToolApplication()
    app.show()
    app.start()
