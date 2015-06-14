__author__ = 'Michael Redmond'


class BoxPicker(object):
    def __init__(self, vtk_widget):
        self._vtk_widget = vtk_widget

    def pick(self, pick_data):
        print 'box picker'
        print pick_data