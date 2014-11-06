__author__ = 'Michael Redmond'


from ..utilities import convert_field


# noinspection PyUnusedLocal
class String(object):
    """String field of a Nastran BDF card.

    """

    def __init__(self, parent=None, index=None, allowable_data=None, can_be_blank=False):
        super(String, self).__init__()

        self.parent = parent
        self.index = index
        self.allowable_data = allowable_data
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
        assert isinstance(value, str)

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

        if self.allowable_data is not None:
            assert (value in self.allowable_data)

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

        _format = '%' + str(self.parent.field_width) + 's'
        return _format % value

    @property
    def default(self):
        default = self.parent.defaults[self.index]
        if default is dict:
            return default['string']
        else:
            return default