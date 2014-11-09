__author__ = 'Michael Redmond'


from .validate_range import ValidateRange
from ..utilities import convert_field


# noinspection PyUnusedLocal
class Integer(ValidateRange):
    """Integer field of a Nastran BDF card.

    """

    __slots__ = ('parent', 'index', 'can_be_blank')

    def __init__(self, parent, parent_cls, name, index=None, min_value=None,
                 max_value=None, ignore_min=False, ignore_max=False, can_be_blank=False):

        super(Integer, self).__init__(parent_cls, name, None, min_value, max_value, ignore_min, ignore_max)

        self.parent = parent
        self.index = index
        self.can_be_blank = can_be_blank
        self._value = '__UNDEFINED__'

    def set_value(self, instance, value):
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

            value = convert_field(value)

        assert isinstance(value, int)

        self.validate_range(value)

        self._value = value

    def __str__(self):
        value = self._value

        try:
            field_width = self.parent.field_width
        except AttributeError:
            field_width = 8

        if value == '__BLANK__' or value == '__UNDEFINED__':
            return ' '*field_width

        str_value = str(value)

        _format = '%' + str(field_width) + 's'
        return _format % str_value

    @property
    def default(self):
        # noinspection PyBroadException
        try:
            return self.default_override()
        except Exception:
            pass

        return self._default

    @property
    def _default(self):
        default = self.parent.defaults[self.index]
        if default is dict:
            return default['int']
        else:
            return default