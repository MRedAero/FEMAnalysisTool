__author__ = 'Michael Redmond'


class Blank(object):
    """Blank field of a Nastran BDF card.

    """

    def __init__(self):
        super(Blank, self).__init__()

        self._value = ''

    # noinspection PyUnusedLocal
    def get_value(self, instance):
        if instance is None:
            return self

        return self._value

    # noinspection PyUnusedLocal
    def set_value(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Blank field must be a string but received '%s'!" % (str(value)))

        if value.replace(' ', '') != '':
            raise ValueError("Blank field must be blank but received '%s'!" % (str(value)))

        self._value = ''

    def __str__(self):
        return ''