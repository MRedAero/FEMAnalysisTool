__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard
from .... import cards


# noinspection PyPep8Naming
class GRID(SimpleCard):
    """Defines the location of a geometric grid point, the directions of its displacement, and
    its permanent single-point constraints.

    """

    card_name = 'GRID'
    category = 'nodes'

    defaults = [None,  # ID
                0,  # CP
                0.,  # X1
                0.,  # X2
                0.,  # X3
                0,  # CD
                None,  # PS
                0  # SEID
                ]

    __slots__ = ('ID', 'CP', 'X1', 'X2', 'X3', 'CD', 'PS', 'SEID',
                 '_ID', '_CP', '_X1', '_X2', '_X3', '_CD', '_PS', '_SEID')

    def __init__(self, data=None):
        super(GRID, self).__init__()

        self._ID = Integer(self, 0, 0, 100000000, True, True)
        self._CP = Integer(self, 1, 0, None, can_be_blank=True)
        self._X1 = Double(self, 2, can_be_blank=True)
        self._X2 = Double(self, 3, can_be_blank=True)
        self._X3 = Double(self, 4, can_be_blank=True)
        self._CD = Integer(self, 5, -1, can_be_blank=True)
        self._PS = Integer(self, 6, 1, 6, can_be_blank=True)
        self._SEID = Integer(self, 7, 0, can_be_blank=True)

        self.field_width = 8

        self.items = [self._ID, self._CP, self._X1, self._X2, self._X3, self._CD, self._PS, self._SEID]

        self.set_data(data)


cards['GRID'] = GRID