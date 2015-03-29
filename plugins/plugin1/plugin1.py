__author__ = 'Michael Redmond'

from .subpackage import some_variable


class Plugin1(object):
    def __init__(self):
        super(Plugin1, self).__init__()

    def some_method(self):
        print some_variable