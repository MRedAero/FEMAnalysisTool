__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard
from .... import cards


# noinspection PyPep8Naming
class CTRIA3(SimpleCard):
    """Defines an iso-parametric membrane-bending or plane strain triangular plate element.

    """

    card_name = 'CTRIA3'
    category = 'elements'

    defaults = [None,  # EID
                None,  # PID
                None,  # G1
                None,  # G2
                None,  # G3
                {'double': 0., 'int': 0},  # THETAorMCID
                0.,  # ZOFFS
                '',  # Blank
                '',  # Blank
                None,  # TFLAG
                1.,  # T1
                1.,  # T2
                1.,  # T3
                ]

    __slots__ = ('EID', 'PID', 'G1', 'G2', 'G3', 'THETAorMCID', 'ZOFFS', 'TFLAG', 'T1', 'T2', 'T3',
                 '_EID', '_PID', '_G1', '_G2', '_G3', '_THETAorMCID', '_ZOFFS', '_Blank1', '_Blank2',
                 '_TFLAG', '_T1', '_T2', '_T3', 'ID', 'THETA', 'MCID')

    # noinspection PyUnresolvedReferences
    def __init__(self, data=None):
        super(CTRIA3, self).__init__()

        self._EID = Integer(self, 0, 0, 100000000, True, True)
        self._PID = Integer(self, 1, 0, 100000000, True, True, can_be_blank=True)
        self._PID.default_override = lambda: self.EID

        self._G1 = Integer(self, 2, 0, 100000000, True, True)
        self._G2 = Integer(self, 3, 0, 100000000, True, True)
        self._G3 = Integer(self, 4, 0, 100000000, True, True)

        double_args = {'name': 'THETA',
                           'min_value': None,
                           'max_value': None,
                           'ignore_min': False,
                           'ignore_max': False,
                           'can_be_blank': True}

        integer_args = {'name': 'MCID',
                        'min_value': None,
                        'max_value': None,
                        'ignore_min': False,
                        'ignore_max': False,
                        'can_be_blank': True}

        self._THETAorMCID = IntegerOrDouble(self, 5, integer_args, double_args)

        self._ZOFFS = Double(self, 6, can_be_blank=True)
        self._Blank1 = Blank()
        self._Blank2 = Blank()
        self._TFLAG = Integer(self, 9, 0, 1, can_be_blank=True)
        self._T1 = Double(self, 10, 0., can_be_blank=True)
        self._T2 = Double(self, 11, 0., can_be_blank=True)
        self._T3 = Double(self, 12, 0., can_be_blank=True)

        self.field_width = 8

        self.items = [self._EID, self._PID, self._G1, self._G2, self._G3, self._THETAorMCID,
                      self._ZOFFS, self._Blank1, self._Blank2, self._TFLAG, self._T1, self._T2, self._T3]

        self.set_data(data)

    @property
    def ID(self):
        # noinspection PyUnresolvedReferences
        return self.EID


cards['CTRIA3'] = CTRIA3