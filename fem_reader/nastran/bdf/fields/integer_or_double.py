__author__ = 'Michael Redmond'

from ..utilities import *
from .integer import Integer
from .double import Double


# noinspection PyUnusedLocal
class IntegerOrDouble(object):
    """Nastran BDF field that can be either an Integer or a Double.

    """

    def __init__(self, parent, parent_cls, name, index=None, integer_args=None, double_args=None):

        super(IntegerOrDouble, self).__init__()

        self.parent = parent

        self._integer_field = Integer(parent, None, None, index, integer_args['min_value'],
                                      integer_args['max_value'], integer_args['ignore_min'], integer_args['ignore_max'],
                                      integer_args['can_be_blank'])
        ":type : .integer.Integer"

        self._double_field = Double(parent, None, None, index, double_args['min_value'],
                                    double_args['max_value'], double_args['ignore_min'], double_args['ignore_max'],
                                    double_args['can_be_blank'])
        ":type : .double.Double"

        self._type = None

        if parent_cls is not None:
            if name is not None:
                setattr(parent_cls, name, property(self.get_value, self.set_value))

            if integer_args['name'] is not None:
                setattr(parent_cls, integer_args['name'], property(self.get_int_value, self.set_int_value))

            if double_args['name'] is not None:
                setattr(parent_cls, double_args['name'], property(self.get_dbl_value, self.set_dbl_value))

    def get_value(self, instance):
        if self._type is None:
            return self._double_field.default

        if self._type is int:
            return self._integer_field.get_value(self._integer_field)
        elif self._type is float:
            return self._double_field.get_value(self._integer_field)

    def set_value(self, instance, value):
        if isinstance(value, str) and value.replace(' ', '') == '':
            value = None
            return

        value = convert_field(value)

        assert (not isinstance(value, str))

        if isinstance(value, int):
            self._integer_field.set_value(self._integer_field, value)
            self._type = int
        elif isinstance(value, float):
            self._double_field.set_value(self._double_field, value)
            self._type = float

    def get_int_value(self, instance):
        tmp = self.get_value(instance)
        if isinstance(tmp, int):
            return tmp
        else:
            return None

    def set_int_value(self, instance, value):
        assert isinstance(value, int)
        self.set_value(instance, value)

    def get_dbl_value(self, instance):
        tmp = self.get_value(instance)
        if isinstance(tmp, float):
            return tmp
        else:
            return None

    def set_dbl_value(self, instance, value):
        assert isinstance(value, float)
        self.set_value(instance, value)

    def __str__(self):
        if self._type is None:
            return ' ' * self.parent.field_width

        if self._type is int:
            return self._integer_field.__str__()
        elif self._type is float:
            return self._double_field.__str__()