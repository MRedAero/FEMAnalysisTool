__author__ = 'Michael Redmond'

"""Various utilities used for reading BDF's.

"""


from math import log10


def convert_field(value):
    """Converts a BDF field to double or integer if it is a string and returns the value.

    """

    if isinstance(value, float) or isinstance(value, int):
        return value

    assert isinstance(value, str)

    if '.' in value:
        try:
            value = float(value)
            return value
        except TypeError:
            raise TypeError('Field has decimal but is not a float! (%s)' % str(value))

    try:
        value = int(value)
        return value
    except TypeError:
            return value


def format_double(value, field_width):
    """Formats a double field.  If the value is too large for the field, it is converted to scientific notation.

    """

    str_value = str(value)
    if len(str_value) > field_width:
        exponent = int(log10(abs(value)))
        small_value = value/10**exponent

        exponent_str = str(exponent)
        if exponent > 0:
            exponent_str = '+' + exponent_str

        what_is_left = field_width - len(exponent_str)

        option = 0

        if small_value >= 1.:
            decimals = what_is_left - 2
        elif small_value >= 0.:
            decimals = what_is_left - 1
            option = 1
        elif small_value <= -1.:
            decimals = what_is_left - 3
        elif small_value > -1.:
            decimals = what_is_left - 2
            option = 2

        # noinspection PyUnboundLocalVariable
        if decimals < 0:
            decimals = 0

        _format = r'%' + str(what_is_left) + r'.' + str(decimals) + 'f'

        str_value = _format % small_value + exponent_str

        if option == 1:
            str_value = str_value[1:]
        elif option == 2:
            str_value = str_value.replace('-0.', '-.')

    return str_value
