__author__ = 'Michael Redmond'


from .double import Double


class DoubleList(object):

    __slots__ = ('parent', 'args', 'data')

    def __init__(self, parent, args):
        super(DoubleList, self).__init__()

        self.parent = parent
        self.args = args

        self.data = []

    def add(self, index, value):
        self.data.insert(index, Double(self, None, None, None, self.args['min_value'],
                                        self.args['max_value'], self.args['ignore_min'],
                                        self.args['ignore_max'], self.args['can_be_blank']))

        self.data[index].default_override = lambda: None

        self.set_value(index, value)

    def delete(self, index):
        del self.data[index]

    def set_value(self, index, value):
        self.data[index].set_value(None, value)

    def get_item(self, index):
        return self.data[index]

    def get_value(self, index):
        return self.data[index].get_value()

    @property
    def field_width(self):
        return self.parent.field_width

    @property
    def size(self):
        return len(self.data)
