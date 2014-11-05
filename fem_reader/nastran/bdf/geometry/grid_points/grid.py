__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard
from .... import cards


# noinspection PyPep8Naming
class GRID(SimpleCard):
    """Defines the location of a geometric grid point, the directions of its displacement, and
    its permanent single-point constraints.

    """

    defaults = [None,  # ID
                0,     # CP
                0.,    # X1
                0.,    # X2
                0.,    # X3
                0,     # CD
                None,  # PS
                0      # SEID
                ]

    card_name = 'GRID'
    category = 'nodes'

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

        if data is not None:
            self.field_width = data[0]
            for i in xrange(1, len(data)):
                self.items[i-1].__set__(self.items[i-1], data[i])

    @property
    def ID(self):
        return self._ID.__get__(self, self._ID)

    @ID.setter
    def ID(self, value):
        self._ID.__set__(self._ID, value)

    @property
    def CP(self):
        return self._CP.__get__(self, self._CP)

    @CP.setter
    def CP(self, value):
        self._CP.__set__(self._CP, value)

    @property
    def X1(self):
        return self._X1.__get__(self, self._X1)

    @X1.setter
    def X1(self, value):
        self._X1.__set__(self._X1, value)

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
    def CD(self):
        return self._CD.__get__(self, self._CD)

    @CD.setter
    def CD(self, value):
        self._CD.__set__(self._CD, value)

    @property
    def PS(self):
        return self._PS.__get__(self, self._PS)

    @PS.setter
    def PS(self, value):
        self._PS.__set__(self._PS, value)

    @property
    def SEID(self):
        return self._SEID.__get__(self, self._SEID)

    @SEID.setter
    def SEID(self, value):
        self._SEID.__set__(self._SEID, value)


cards['GRID'] = GRID