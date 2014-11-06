__author__ = 'Michael Redmond'


from ..utilities import *


# noinspection PyUnusedLocal
class StringOrDouble(object):
    """Nastran BDF field that can be either a String or a Double.

    """

    def __init__(self, parent=None, string_field=None, double_field=None):
        super(StringOrDouble, self).__init__()

        self.parent = parent
        self._string_field = string_field
        ":type : .string.String"
        self._double_field = double_field
        ":type : .double.Double"
        self._type = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self._type is None:
            return self._double_field.default

        if self._type is str:
            return self._string_field
        elif self._type is float:
            return self._double_field

    def __set__(self, instance, value):
        if isinstance(value, str) and value.replace(' ', '') == '':
            value = None
            return

        value = convert_field(value)

        assert (not isinstance(value, int))

        if isinstance(value, str):
            self._string_field = value
            self._type = str
        elif isinstance(value, float):
            self._double_field = value
            self._type = float

    def __str__(self):
        if self._type is None:
            return ' '*self.parent.field_width

        if self._type is str:
            return self._string_field.__str__()
        elif self._type is float:
            return self._double_field.__str__()