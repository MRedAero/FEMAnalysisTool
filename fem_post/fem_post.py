__author__ = 'Michael Redmond'

# modifies sys.path for external_tools
import external_tools

from application import FEMAnalysisToolApplication


def main():
    app = FEMAnalysisToolApplication()
    app.show()
    app.start()