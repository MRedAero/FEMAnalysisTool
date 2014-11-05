__author__ = 'Michael Redmond'


from .validate_range import ValidateRange
from ..utilities import *


# noinspection PyUnusedLocal
class Double(ValidateRange):
    """Double field of a Nastran BDF card.

    """

    def __init__(self, parent=None, index=None, min_value=None, max_value=None, ignore_min=False,
                 ignore_max=False, can_be_blank=False):
        super(Double, self).__init__(min_value, max_value, ignore_min, ignore_max)

        self.parent = parent
        self.index = index
        self.can_be_blank = can_be_blank
        self._value = '__UNDEFINED__'

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self._value == '__UNDEFINED__' or self._value == '__BLANK__':
            if self.default is not None:
                return self.default
            else:
                return ''

        if self._value == '__DEFAULT__':
            return self.default

        return self._value

    def __set__(self, instance, value):
        if isinstance(value, str):
            if value.replace(' ', '') == '':
                if self.can_be_blank:
                    self._value = '__BLANK__'
                    return
                else:
                    if self.default is not None:
                        self._value = '__DEFAULT__'
                        return
                    else:
                        raise ValueError('Integer field cannot be blank!')

            if '.' not in value:
                raise TypeError('Double must have a decimal point! (%s)' % value)

            value = value.strip()

            value = value[0] + value[1:].replace('-', 'E-').replace('+', 'E+')

            try:
                value = float(value)
            except Exception:
                raise TypeError("Cannot convert '%s' to double!" % value)

        assert isinstance(value, float)

        self.validate_range(value)

        self._value = value

    def __str__(self):
        value = self._value

        field_width = self.parent.field_width

        if value == '__BLANK__' or value == '__UNDEFINED__':
            return ' '*field_width

        #if value == '__UNDEFINED__':
        #    if self.default is None:
        #        return ' '*self.parent.field_width
        #    else:
        #        value = self.default

        str_value = format_double(value, field_width)

        _format = '%' + str(field_width) + 's'
        return _format % str_value

    @property
    def default(self):
        default = self.parent.defaults[self.index]
        if default is dict:
            return default['double']
        else:
            return default
