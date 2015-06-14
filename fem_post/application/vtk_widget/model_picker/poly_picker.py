__author__ = 'Michael Redmond'


class PolyPicker(object):
    def __init__(self, vtk_widget):
        self._vtk_widget = vtk_widget

    def pick(self, pick_data):
        print 'poly picker'
        print pick_data