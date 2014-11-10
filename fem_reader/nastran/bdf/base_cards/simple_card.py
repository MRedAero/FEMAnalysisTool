__author__ = 'Michael Redmond'


class SimpleCard(object):
    """Abstract class for the simplest type of bdf card.

    """

    card_name = 'Simple'

    __slots__ = ('items', 'field_width')

    def __init__(self):
        super(SimpleCard, self).__init__()

        self.items = []
        self.field_width = 8

    def set_data(self, data):
        if data is not None:
            self.field_width = data[0]
            for i in xrange(1, len(data)):
                self.items[i-1].set_value(self.items[i-1], data[i])

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
                result += current_line + cont.strip() + '\n'
                current_line = cont

            #current_line += _format % self.items[i].__str__()
            current_line += self.items[i].__str__()

        if current_line != cont:
            result += current_line + '\n'

        while result[-1] == r'*' or result[-1] == '\n':
            result = result[:-1]

        return result