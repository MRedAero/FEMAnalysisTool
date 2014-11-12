__author__ = 'Michael Redmond'


class GenericField(object):
    """Abstract class subclassed by ValidateRange and String.

    """

    __slots__ = ('_value', 'default_override')

    def __init__(self, parent_cls, name, value=None):
        super(GenericField, self).__init__()

        self._value = value

        self.default_override = None

    # noinspection PyUnusedLocal
    @property
    def value(self):
        if self._value == '__UNDEFINED__' or self._value == '__BLANK__':
            if self.default is not None:
                return self.default
            else:
                return ''

        if self._value == '__DEFAULT__':
            return self.default

        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def default(self):
        raise NotImplementedError

    def __str__(self):
        return str(self._value)