__author__ = 'Michael Redmond'


from .generic_field import GenericField


# noinspection PyUnusedLocal
class String(GenericField):
    """String field of a Nastran BDF card.

    """

    __slots__ = ('parent', 'index', 'allowable_data', 'can_be_blank')

    def __init__(self, parent, parent_cls, name, index=None, allowable_data=None, can_be_blank=False):

        super(String, self).__init__(parent_cls, name, None)

        self.parent = parent
        self.index = index
        self.allowable_data = allowable_data
        self.can_be_blank = can_be_blank
        self._value = '__UNDEFINED__'

    def set_value(self, instance, value):
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
                    raise ValueError('String field cannot be blank!')

        if self.allowable_data is not None:
            try:
                assert (value.strip() in self.allowable_data)
            except AssertionError:
                raise AssertionError("'%s' not an allowed value!" % value.strip())

        self._value = value

    def __str__(self):
        value = self._value

        try:
            field_width = self.parent.field_width
        except AttributeError:
            field_width = 8

        if value == '__BLANK__' or value == '__UNDEFINED__':
            return ' '*field_width

        return value.strip().rjust(field_width, ' ')

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
            return default['string']
        else:
            return default