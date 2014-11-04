__author__ = 'Michael Redmond'


from .validate_range import ValidateRange


# noinspection PyUnusedLocal
class Integer(ValidateRange):
    """Integer field of a Nastran BDF card.

    """

    def __init__(self, parent=None, index=None, min_value=None, max_value=None, ignore_min=False,
                 ignore_max=False, can_be_blank=False):
        super(Integer, self).__init__(min_value, max_value, ignore_min, ignore_max)

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

            if r'.' in value:
                raise TypeError('Integer cannot have a decimal point! (%s)' % value)

            try:
                value = int(value)
            except Exception:
                raise TypeError("Cannot convert '%s' to integer!" % value)

        assert isinstance(value, int)

        self.validate_range(value)

        self._value = value

    def __str__(self):
        value = self._value

        if value == '__BLANK__':
            return ' '*self.parent.field_width

        if value == '__UNDEFINED__':
            if self.default is None:
                return ' '*self.parent.field_width
            else:
                value = self.default

        str_value = str(value)

        #if len(str_value) <= self.parent.field_width:
        #    format = '%' + str(self.parent.field_width) + 's'
        #    return format % str_value

        _format = '%' + str(self.parent.field_width) + 's'
        return _format % str_value

    @property
    def default(self):
        default = self.parent.defaults[self.index]
        if default is dict:
            return default['int']
        else:
            return default