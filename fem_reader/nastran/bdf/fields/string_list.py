__author__ = 'Michael Redmond'


from .string import String


class StringList(object):

    __slots__ = ('parent', 'args', 'data')

    def __init__(self, parent, args):
        super(StringList, self).__init__()

        self.parent = parent
        self.args = args

        self.data = []

    def add(self, index, value):
        self.data.insert(index, String(self, None, self.args['allowable_data'], self.args['can_be_blank']))

        self.data[index].default_override = lambda: None

        self.set_value(index, value)

    def delete(self, index):
        del self.data[index]

    def set_value(self, index, value):
        self.data[index].value = value

    def get_value(self, index):
        return self.data[index].value

    def get_item(self, index):
        return self.data[index]

    @property
    def field_width(self):
        return self.parent.field_width

    @property
    def size(self):
        return len(self.data)
