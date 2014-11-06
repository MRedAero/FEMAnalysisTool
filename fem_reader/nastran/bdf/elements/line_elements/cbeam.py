__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard
from .... import cards


# noinspection PyPep8Naming
class CBEAM(SimpleCard):
    """Defines a beam element.

    """

    defaults = [None,  # EID
                None,  # PID
                None,  # GA
                None,  # GB
                {'double': None, 'int': None},  # X1orG0
                None,  # X2
                None,  # X3
                {'string': '__BLANK__', 'double': 0.},    # OFFT_BIT
                None,  # PA
                None,  # PB
                None,  # W1A
                None,  # W2A
                None,  # W3A
                None,  # W1B
                None,  # W2B
                None,  # W3B
                None,  # SA
                None,  # SB
    ]

    card_name = 'CBEAM'
    category = 'elements'

    def __init__(self, data=None):
        super(CBEAM, self).__init__()

        self._EID = Integer(self, 0, 0, 100000000, True, True)
        self._PID = Integer(self, 1, 0, 100000000, True, True, can_be_blank=True)
        self._GA = Integer(self, 2, 0, 100000000, True, True)
        self._GB = Integer(self, 3, 0, 100000000, True, True)
        _x1 = Double(self, 4, can_be_blank=True)
        _g0 = Integer(self, 4, 0, None, True, True, can_be_blank=True)
        self._X1orG0 = IntegerOrDouble(self, _x1, _g0)
        self._X2 = Double(self, 5, can_be_blank=True)
        self._X3 = Double(self, 6, can_be_blank=True)
        _offt = String(self, 7, ['GGG', 'BGG', 'GGO', 'BGO', 'GOG', 'BOG', 'GOO', 'BOO'], can_be_blank=True)
        _bit = Double(self, 7, can_be_blank=True)
        self._OFFT_BIT = StringOrDouble(self, _offt, _bit)
        self._PA = Integer(self, 8, 1, 6, can_be_blank=True)
        self._PB = Integer(self, 9, 1, 6, can_be_blank=True)
        self._W1A = Double(self, 10, can_be_blank=True)
        self._W2A = Double(self, 11, can_be_blank=True)
        self._W3A = Double(self, 12, can_be_blank=True)
        self._W1B = Double(self, 13, can_be_blank=True)
        self._W2B = Double(self, 14, can_be_blank=True)
        self._W3B = Double(self, 15, can_be_blank=True)
        self._SA = Integer(self, 16, 0, can_be_blank=True)
        self._SB = Integer(self, 16, 0, can_be_blank=True)

        self.field_width = 8

        self.items = [self._EID, self._PID, self._GA, self._GB, self._X1orG0, self._X2, self._X3,
                      self._OFFT_BIT, self._PA, self._PB, self._W1A, self._W2A, self._W3A, self._W1B,
                      self._W2B, self._W3B, self._SA, self._SB]

        if data is not None:
            self.field_width = data[0]
            for i in xrange(1, len(data)):
                self.items[i-1].__set__(self.items[i-1], data[i])

    @property
    def ID(self):
        return self._EID.__get__(self, self._EID)

    @property
    def EID(self):
        return self._EID.__get__(self, self._EID)

    @EID.setter
    def EID(self, value):
        self._EID.__set__(self._EID, value)

    @property
    def PID(self):
        pid = self._PID.__get__(self, self.PID)

        # The default value for PID is EID.
        if pid is None:
            return self._EID.__get__(self, self._EID)
        else:
            return pid

    @PID.setter
    def PID(self, value):
        self._PID.__set__(self._PID, value)

    @property
    def GA(self):
        return self._GA.__get__(self, self._GA)

    @GA.setter
    def GA(self, value):
        self._GA.__set__(self._GA, value)

    @property
    def GB(self):
        return self._GB.__get__(self, self._GB)

    @GB.setter
    def GB(self, value):
        self._GB.__set__(self._GB, value)

    @property
    def X1(self):
        tmp = self._X1orG0.__get__(self, self._X1orG0)
        if isinstance(tmp, float):
            return tmp
        else:
            return None

    @X1.setter
    def X1(self, value):
        assert isinstance(value, float)
        self._X1orG0.__set__(self._X1orG0, value)

    @property
    def G0(self):
        tmp = self._X1orG0.__get__(self, self._X1orG0)
        if isinstance(tmp, int):
            return tmp
        else:
            return None

    @G0.setter
    def G0(self, value):
        assert isinstance(value, int)
        self._X1orG0.__set__(self._X1orG0, value)

    @property
    def X2(self):
        return self._X2.__get__(self, self._X2)

    @X2.setter
    def X2(self, value):
        self._X2.__set__(self._X2, value)

    @property
    def X3(self):
        return self._X3.__get__(self, self._X3)

    @X3.setter
    def X3(self, value):
        self._X3.__set__(self._X3, value)

    @property
    def OFFT_BIT(self):
        return self._OFFT_BIT.__get__(self, self._OFFT_BIT)

    @OFFT_BIT.setter
    def OFFT_BIT(self, value):
        self._OFFT_BIT.__set__(self._OFFT_BIT, value)

    @property
    def PA(self):
        return self._PA.__get__(self, self._PA)

    @PA.setter
    def PA(self, value):
        self._PA.__set__(self._PA, value)

    @property
    def PB(self):
        return self._PB.__get__(self, self._PB)

    @PB.setter
    def PB(self, value):
        self._PB.__set__(self._PB, value)

    @property
    def W1A(self):
        return self._W1A.__get__(self, self._W1A)

    @W1A.setter
    def W1A(self, value):
        self._W1A.__set__(self._W1A, value)

    @property
    def W2A(self):
        return self._W2A.__get__(self, self._W2A)

    @W2A.setter
    def W2A(self, value):
        self._W2A.__set__(self._W2A, value)

    @property
    def W3A(self):
        return self._W3A.__get__(self, self._W3A)

    @W3A.setter
    def W3A(self, value):
        self._W3A.__set__(self._W3A, value)

    @property
    def W1B(self):
        return self._W1B.__get__(self, self._W1B)

    @W1B.setter
    def W1B(self, value):
        self._W1B.__set__(self._W1B, value)

    @property
    def W2B(self):
        return self._W2B.__get__(self, self._W2B)

    @W2B.setter
    def W2B(self, value):
        self._W2B.__set__(self._W2B, value)

    @property
    def W3B(self):
        return self._W3B.__get__(self, self._W3B)

    @W3B.setter
    def W3B(self, value):
        self._W3B.__set__(self._W3B, value)

    @property
    def SA(self):
        return self._SA.__get__(self, self._SA)

    @SA.setter
    def SA(self, value):
        self._SA.__set__(self._SA, value)

    @property
    def SB(self):
        return self._SB.__get__(self, self._SB)

    @SB.setter
    def SB(self, value):
        self._SB.__set__(self._SB, value)


cards['CBEAM'] = CBEAM