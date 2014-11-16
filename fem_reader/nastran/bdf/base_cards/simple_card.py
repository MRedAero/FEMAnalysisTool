__author__ = 'Michael Redmond'


class SimpleCard(object):
    """Abstract class for the simplest type of bdf card.

    """

    card_name = 'Simple'

    __slots__ = ('items', 'field_width', 'model')

    def __init__(self, model=None):
        super(SimpleCard, self).__init__()

        self.model = model

        self.items = []
        self.field_width = 8

    def set_data(self, data):
        if data is not None:
            self.field_width = data[0]
            try:
                for i in xrange(1, len(data)):
                    self.items[i-1].value = data[i]
            except IndexError:
                pass

    def __getattr__(self, name):
        # this is only used when the attribute 'name' does not currently exist
        # a property will be created to access the value of attribute, _name.value

        hidden_attr = '_%s' % name

        def _get_value(self_):
            return self_.__getattribute__(hidden_attr).value

        def _set_value(self_, value):
            self_.__getattribute__(hidden_attr).value = value

        setattr(SimpleCard, name, property(_get_value, _set_value))
        return self.__getattribute__(hidden_attr).value

    def __str__(self):
        if self.field_width == 16:
            card_name = self.card_name + r'*'
            cont = r'*       '
        else:
            card_name = self.card_name
            cont = r'        '

        current_line = '%-8s' % card_name

        result = ''

        #_format = '%+' + str(self.field_width) + 's'

        for i in xrange(len(self.items)):
            if len(current_line) >= 72:
                if current_line[8:64].strip() == '':
                    current_line = cont
                    break  # is this ok or will data be missing?  pretty sure no blank lines are allowed
                result += current_line + cont.strip() + '\n'
                current_line = cont

            #current_line += _format % self.items[i].__str__()
            current_line += self.items[i].__str__()

        if current_line != cont:
            if current_line[8:64].strip() != '':
                result += current_line + '\n'

        while result[-1] == r'*' or result[-1] == '\n':
            result = result[:-1]

        return result