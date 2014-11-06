__author__ = 'Michael Redmond'


from collections import OrderedDict
from ... import cards
from ..utilities import convert_field


class BDF(object):
    def __init__(self):
        super(BDF, self).__init__()

        self.elements = OrderedDict()
        self.nodes = OrderedDict()
        self.coordinate_systems = OrderedDict()
        self.materials = OrderedDict()
        self.properties = OrderedDict()
        self.loads = OrderedDict()
        self.constraints = OrderedDict()


class BDFReader(object):
    def __init__(self):
        super(BDFReader, self).__init__()

        self._data = None
        self._data_keys = None
        self._level = 0

        self._card_keys = cards.keys()

        #print self._card_keys

    def read_bdf(self, filename):

        try:
            _file = open(filename, 'r')
        except IOError:
            raise IOError("File '%s' does not exist!" % filename)

        if self._data is None:
            self._data = BDF()
            self._data_keys = {}
            self._data_keys['elements'] = self._data.__getattribute__('elements')
            self._data_keys['nodes'] = self._data.__getattribute__('nodes')
            self._data_keys['coordinate_systems'] = self._data.__getattribute__('coordinate_systems')
            # add others

        lines = _file.read().split('\n')
        _file.close()

        #cdef int i, j, continuations, line_size, goto

        line_size = len(lines)

        continuations = 0

        goto = 0

        self._level += 1

        for i in xrange(line_size):

            #print i

            if continuations:
                continuations -= 1
                continue

            line = remove_comments(lines[i])

            goto = 2

            if line[0:7] == 'INCLUDE':

                goto = 1

                include_line = line

                continuations = 0
                for j in xrange(i+1, line_size):
                    if include_line.count("'") == 2:
                        break

                    continuations += 1
                    include_line += remove_comments(lines[j])

            if goto == 1:
                #print 'goto = 1'
                include_file = include_line.split("'")[1]
                self.read_bdf(include_file)
                continue

            if goto == 2:
                #print 'goto = 2'
                card = line[0:8].strip()

                if r'*' in card:
                    field_width = 16
                else:
                    field_width = 8

                card = card.replace(r'*', '')

                #print card

                if card in self._card_keys:
                    card_line = '%-64s' % line[8:72]

                    bdf_line = i

                    try:
                        cont = line[72:81].strip()
                    except Exception:
                        cont = ''

                    goto = 3

                    continuations = 0
                    for j in xrange(i+1, line_size):
                        line = remove_comments(lines[j])

                        if line[0:8].strip() == cont:
                            card_line += '%-64s' % line[8:72]
                            continuations += 1
                        else:
                            break

                        try:
                            cont = line[72:81].strip()
                        except Exception:
                            cont = ''

            if goto == 3:
                #print 'goto = 3'
                if ',' in card_line:
                    data = map(convert_field, parse_string(card_line, ','))
                else:
                    data = map(convert_field, parse_string_fixed_width(card_line, field_width))

                data.insert(0, field_width)

                try:
                    new_data = cards[card](data)
                except Exception:
                    print 'BDF %s: line %d: field_width = %d\n%s' % (filename, bdf_line+1, field_width, card_line)
                    raise

                self._data_keys[new_data.category][new_data.ID] = new_data

                goto = 0

        self._level -= 1

        if self._level == 0:
            return self._data


def parse_string(in_str, parse):
    return in_str.split(parse)


import re

def parse_string_fixed_width(in_str, width):
    return re.findall('.{%d}' % width, in_str)


def remove_comments(line):
    index = line.find(r'$')
    if index < 1:
        index = len(line)

    return line[0:index]

