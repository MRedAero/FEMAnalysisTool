__author__ = 'Michael Redmond'

import os

python = r"D:\WinPython-64bit-2.7.6.4\python-2.7.6.amd64\python.exe"
uic = r"D:\WinPython-64bit-2.7.6.4\python-2.7.6.amd64\Lib\site-packages\PyQt4\uic\pyuic.py"

os.system('%s %s -o vtk_selections_test.py vtk_selections_test_ui.ui' % (python, uic))