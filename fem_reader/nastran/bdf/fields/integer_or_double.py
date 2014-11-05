__author__ = 'Michael Redmond'


from ..utilities import *


# noinspection PyUnusedLocal
class IntegerOrDouble(object):
    """Nastran BDF field that can be either an Integer or a Double.

    """

    def __init__(self, parent=None, integer_field=None, double_field=None):
        super(IntegerOrDouble, self).__init__()

        self.parent = parent
        self._integer_field = integer_field
        ":type : .integer.Integer"
        self._double_field = double_field
        ":type : .double.Double"
        self._type = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self._type is None:
            return self._double_field.default

        if self._type is int:
            return self._integer_field
        elif self._type is float:
            return self._double_field

    def __set__(self, instance, value):
        if isinstance(value, str) and value.replace(' ', '') == '':
            value = None
            return

        value = convert_field(value)

        assert (not isinstance(value, str))

        if isinstance(value, int):
            self._integer_field = value
            self._type = int
        elif isinstance(value, float):
            self._double_field = value
            self._type = float

    def __str__(self):
        if self._type is None:
            return ' '*self.parent.field_width

        if self._type is int:
            return self._integer_field.__str__()
        elif self._type is float:
            return self._double_field.__str__()