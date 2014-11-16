__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard
from .... import cards


# noinspection PyPep8Naming
class CBEAM(SimpleCard):
    """Defines a beam element.

    """

    card_name = 'CBEAM'
    category = 'elements'

    defaults = [None,  # EID
                None,  # PID
                None,  # GA
                None,  # GB
                {'double': None, 'int': None},  # X1orG0
                None,  # X2
                None,  # X3
                {'string': '__BLANK__', 'double': 0.},  # OFFT_BIT
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

    __slots__ = ('EID', 'PID', 'GA', 'GB', 'X1orG0', 'X2', 'X3', 'OFFT_BIT', 'PA', 'PB', 'W1A', 'W2A', 'W3A',
                 'W1B', 'W2B', 'W3B', 'SA', 'SB', '_EID', '_PID', '_GA', '_GB', '_X1orG0', '_X2', '_X3', '_OFFT_BIT',
                 '_PA', '_PB', '_W1A', '_W2A', '_W3A', '_W1B', '_W2B', '_W3B', '_SA', '_SB', 'ID', 'X1', 'G0', 'OFFT',
                 'BIT')

    def __init__(self, model=None, data=None):
        super(CBEAM, self).__init__(model)

        self._EID = Integer(self, 0, 0, 100000000, True, True)
        self._PID = Integer(self, 1, 0, 100000000, True, True, can_be_blank=True)
        self._GA = Integer(self, 2, 0, 100000000, True, True)
        self._GB = Integer(self, 3, 0, 100000000, True, True)

        double_args = {'name': 'X1',
                       'min_value': None,
                       'max_value': None,
                       'ignore_min': False,
                       'ignore_max': False,
                       'can_be_blank': True}

        integer_args = {'name': 'G0',
                        'min_value': 0,
                        'max_value': None,
                        'ignore_min': True,
                        'ignore_max': True,
                        'can_be_blank': True}

        self._X1orG0 = IntegerOrDouble(self, 4, integer_args, double_args)

        self._X2 = Double(self, 5, can_be_blank=True)
        self._X3 = Double(self, 6, can_be_blank=True)

        string_args = {'name': 'OFFT',
                       'allowable_data': ['GGG', 'BGG', 'GGO', 'BGO', 'GOG', 'BOG', 'GOO', 'BOO'],
                       'can_be_blank': True}

        double_args = {'name': 'BIT',
                       'min_value': None,
                       'max_value': None,
                       'ignore_min': False,
                       'ignore_max': False,
                       'can_be_blank': True}

        self._OFFT_BIT = StringOrDouble(self, 7, string_args, double_args)

        self._PA = Integer(self, 8, 1, 6, can_be_blank=True)
        self._PB = Integer(self, 9, 1, 6, can_be_blank=True)
        self._W1A = Double(self, 10, can_be_blank=True)
        self._W2A = Double(self, 11, can_be_blank=True)
        self._W3A = Double(self, 12, can_be_blank=True)
        self._W1B = Double(self, 13, can_be_blank=True)
        self._W2B = Double(self, 14, can_be_blank=True)
        self._W3B = Double(self, 15, can_be_blank=True)
        self._SA = Integer(self, 16, 0, can_be_blank=True)
        self._SB = Integer(self, 17, 0, can_be_blank=True)

        self.field_width = 8

        self.items = [self._EID, self._PID, self._GA, self._GB, self._X1orG0, self._X2, self._X3,
                      self._OFFT_BIT, self._PA, self._PB, self._W1A, self._W2A, self._W3A, self._W1B,
                      self._W2B, self._W3B, self._SA, self._SB]

        self.set_data(data)

    @property
    def ID(self):
        # noinspection PyUnresolvedReferences
        return self.EID

    @property
    def nodes(self):
        return [self.GA, self.GB]


cards['CBEAM'] = CBEAM