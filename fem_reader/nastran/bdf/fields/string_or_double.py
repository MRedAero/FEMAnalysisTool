__author__ = 'Michael Redmond'


from ..utilities import *
from .string import String
from .double import Double


# noinspection PyUnusedLocal
class StringOrDouble(object):
    """Nastran BDF field that can be either a String or a Double.

    """

    def __init__(self, parent, index=None, string_args=None, double_args=None):
        super(StringOrDouble, self).__init__()

        self.parent = parent

        self._string_field = String(parent, index, string_args['allowable_data'],
                                    string_args['can_be_blank'])

        ":type : .string.String"

        self._double_field = Double(parent, index, double_args['min_value'],
                                    double_args['max_value'], double_args['ignore_min'], double_args['ignore_max'],
                                    double_args['can_be_blank'])
        ":type : .double.Double"

        self._type = None

        #if parent_cls is not None:
        #    if name is not None:
        #        setattr(parent_cls, name, property(self.get_value, self.set_value))
        #
        #    if string_args['name'] is not None:
        #        setattr(parent_cls, string_args['name'], property(self.get_str_value, self.set_str_value))
        #
        #    if double_args['name'] is not None:
        #        setattr(parent_cls, double_args['name'], property(self.get_dbl_value, self.set_dbl_value))

    def get_value(self, instance):
        if self._type is None:
            return self._double_field.default

        if self._type is str:
            return self._string_field
        elif self._type is float:
            return self._double_field

    def set_value(self, instance, value):
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

    def get_str_value(self, instance):
        tmp = self.get_value(instance)
        if isinstance(tmp, str):
            return tmp
        else:
            return None

    def set_str_value(self, instance, value):
        assert isinstance(value, str)
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
            return ' '*self.parent.field_width

        if self._type is str:
            return self._string_field.__str__()
        elif self._type is float:
            return self._double_field.__str__()