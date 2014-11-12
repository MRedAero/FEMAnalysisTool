__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard
from .... import cards


# noinspection PyPep8Naming
class PCOMP(SimpleCard):
    """Defines the properties of an n-ply composite material laminate.

    """

    card_name = 'PCOMP'
    category = 'properties'

    defaults = [None,  # PID
                None,  # Z0
                None,  # NSM
                None,  # SB
                '__BLANK__',  # FT
                0.,  # TREF
                0.,  # GE
                '__BLANK__',  # LAM
    ]

    __slots__ = ('PID', 'Z0', 'NSM', 'SB', 'FT', 'TREF', 'GE', 'LAM',
                 '_PID', '_Z0', '_NSM', '_SB', '_FT', '_TREF', '_GE', '_LAM', '_MID', '_T', '_THETA', '_SOUT')

    def __init__(self, data=None):
        super(PCOMP, self).__init__()

        self._PID = Integer(self, 0, 0, 100000000, True, True)

        self._Z0 = Double(self, 1, can_be_blank=True)
        self._Z0.default_override = lambda: -0.5 * self.thickness

        self._NSM = Double(self, 2, can_be_blank=True)
        self._SB = Double(self, 3, 0., can_be_blank=True)
        self._FT = String(self, 4, ['HILL', 'HOFF', 'TSAI', 'STRN'], can_be_blank=True)
        self._TREF = Double(self, 5, can_be_blank=True)
        self._GE = Double(self, 6, can_be_blank=True)
        self._LAM = String(self, 7, ['SYM', 'MEM', 'BEND', 'SMEAR', 'SMCORE'], can_be_blank=True)

        self._MID = IntegerList(self, {'min_value': 0,
                                       'max_value': None,
                                       'ignore_min': True,
                                       'ignore_max': False,
                                       'can_be_blank': False})

        self._T = DoubleList(self, {'min_value': None,
                                    'max_value': None,
                                    'ignore_min': True,
                                    'ignore_max': False,
                                    'can_be_blank': True})

        self._THETA = DoubleList(self, {'min_value': None,
                                        'max_value': None,
                                        'ignore_min': True,
                                        'ignore_max': False,
                                        'can_be_blank': True})

        self._SOUT = StringList(self, {'allowable_data': ['YES', 'NO'],
                                       'can_be_blank': True})

        self.field_width = 8

        self.items = [self._PID, self._Z0, self._NSM, self._SB, self._FT, self._TREF, self._GE, self._LAM]

        self.set_data(data)

    def set_data(self, data):
        # first 8 fields

        super(PCOMP, self).set_data(data[0:9])

        # ply data
        data = data[9:]

        plies = divmod(len(data), 4)

        missing = plies[1]

        for i in xrange(missing):
            data.append(' '*self.field_width)

        #print data

        while True:
            try:
                if str(data[-1] + data[-2] + data[-3] + data[-4]).strip() == '':
                    #print 'delete'
                    data = data[0:-4]
                else:
                    break
            except Exception:
                break

        plies = divmod(len(data), 4)[0]

        #print data

        j = 0
        for i in xrange(plies):
            self._MID.add(i, data[j])
            self._T.add(i, data[j+1])
            self._THETA.add(i, data[j+2])
            self._SOUT.add(i,data[j+3])

            j += 4

    @property
    def ID(self):
        return self.PID

    @property
    def thickness(self):
        t = 0.
        for i in xrange(self._T.size):
            t += self._T.get_value(i)

        return t

    def MID(self, index):
        return self._MID.get_value(index)

    def T(self, index):
        tmp = self._T.get_value(index)
        if isinstance(tmp, float):
            return tmp

        while index > 0:
            index -= 1
            tmp = self._T.get_value(index)
        if isinstance(tmp, float):
            return tmp

        return None

    def THETA(self, index):
        tmp = self._THETA.get_value(index)
        if isinstance(tmp, float):
            return tmp

        return 0.

    def SOUT(self, index):
        tmp = self._SOUT.get_value(index)
        if tmp in ['YES', 'NO']:
            return tmp

        return 'NO'

    def __str__(self):
        if self.field_width == 16:
            card_name = self.card_name + r'*'
            cont = r'*       '
        else:
            card_name = self.card_name
            cont = r'        '

        tmp = super(PCOMP, self).__str__().split('\n')

        current_line = tmp[-1][0:72]

        result = ''

        for i in xrange(len(tmp)-1):
            result += tmp[i] + '\n'

        #_format = '%+' + str(self.field_width) + 's'

        for i in xrange(self._MID.size):
            if len(current_line) >= 72:
                result += current_line + cont.strip() + '\n'
                current_line = cont

            current_line += self._MID.get_item(i).__str__()

            if len(current_line) >= 72:
                result += current_line + cont.strip() + '\n'
                current_line = cont

            current_line += self._T.get_item(i).__str__()

            if len(current_line) >= 72:
                result += current_line + cont.strip() + '\n'
                current_line = cont

            current_line += self._THETA.get_item(i).__str__()

            if len(current_line) >= 72:
                result += current_line + cont.strip() + '\n'
                current_line = cont

            current_line += self._SOUT.get_item(i).__str__()

        if current_line != cont:
            result += current_line + '\n'

        result = result.rstrip()

        while result[-1:] == r'*':
            result = result[:-1].rstrip()

        return result


cards['PCOMP'] = PCOMP