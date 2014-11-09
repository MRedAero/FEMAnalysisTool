__author__ = 'Michael Redmond'


from .generic_field import GenericField


class ValidateRange(GenericField):
    """Abstract class for Double and Integer fields to validate ranges.  This class is NOT a field but is meant
    to be subclassed by Double and Integer classes.

    """

    __slots__ = ('_min', '_max', '_ignore_min', '_ignore_max')

    def __init__(self, parent_cls, name, value=None, min_value=None,
                 max_value=None, ignore_min=False, ignore_max=False):

        super(ValidateRange, self).__init__(parent_cls, name, value)

        self._min = min_value
        self._max = max_value
        self._ignore_min = ignore_min
        self._ignore_max = ignore_max

    def validate_range(self, value):
        if self._min is not None:
            if self._ignore_min:
                if not (self._min < value):
                    raise ValueError('Range value must be greater than %s but is %s!' % (str(self._min), str(value)))
            else:
                if not (self._min <= value):
                    raise ValueError('Range value must be greater than or equal to %s but is %s!' %
                                     (str(self._min), str(value)))

        if self._max is not None:
            if self._ignore_max:
                if not (self._max > value):
                    raise ValueError('Range value must be less than %s but is %s!' % (str(self._max), str(value)))
            else:
                if not (self._max >= value):
                    raise ValueError('Range value must be less than or equal to %s but is %s!' %
                                     (str(self._max), str(value)))