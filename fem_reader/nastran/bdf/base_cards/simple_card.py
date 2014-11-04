__author__ = 'Michael Redmond'


class SimpleCard(object):
    """Abstract class for the simplest type of bdf card.

    """

    card_name = 'Simple'

    def __init__(self):
        super(SimpleCard, self).__init__()

        self.items = []
        self.field_width = 8

    def __str__(self):
        if self.field_width == 16:
            card_name = self.card_name + r'*'
        else:
            card_name = self.card_name

        current_line = '%-8s' % card_name

        result = ''

        format = '%+' + str(self.field_width) + 's'

        for i in xrange(len(self.items)):
            if len(current_line) >= 72:
                result += current_line + '\n'
                current_line = ' '*8

            current_line += format % self.items[i].__str__()

        if current_line != ' '*8:
            result += current_line + '\n'

        return result