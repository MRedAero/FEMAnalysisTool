__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard


# noinspection PyPep8Naming
class CTRIA3(SimpleCard):
    """Defines an iso-parametric membrane-bending or plane strain triangular plate element.

    """

    defaults = [None,  # EID
                None,  # PID
                None,  # G1
                None,  # G2
                None,  # G3
                {'double': 0., 'int': 0},  # ThetaOrMCID
                0.,    # ZOFFS
                '',    # Blank
                '',    # Blank
                None,  # TFLAG
                1.,  # T1
                1.,  # T2
                1.,  # T3
    ]

    card_name = 'CTRIA3'
    category = 'elements'

    def __init__(self, data=None):
        super(CTRIA3, self).__init__()

        self._EID = Integer(self, 0, 0, 100000000, True, True)
        self._PID = Integer(self, 1, 0, 100000000, True, True, can_be_blank=True)
        self._G1 = Integer(self, 2, 0, 100000000, True, True)
        self._G2 = Integer(self, 3, 0, 100000000, True, True)
        self._G3 = Integer(self, 4, 0, 100000000, True, True)
        theta = Double(self, 5, can_be_blank=True)
        mcid = Integer(self, 5, can_be_blank=True)
        self._ThetaOrMCID = IntegerOrDouble(self, mcid, theta)
        self._ZOFFS = Double(self, 6, can_be_blank=True)
        self._Blank1 = Blank()
        self._Blank2 = Blank()
        self._TFLAG = Integer(self, 9, 0, 1, can_be_blank=True)
        self._T1 = Double(self, 10, 0., can_be_blank=True)
        self._T2 = Double(self, 11, 0., can_be_blank=True)
        self._T3 = Double(self, 12, 0., can_be_blank=True)

        self.field_width = 8

        self.items = [self._EID, self._PID, self._G1, self._G2, self._G3, self._ThetaOrMCID,
                      self._ZOFFS, self._Blank1, self._Blank2, self._TFLAG, self._T1, self._T2, self._T3]

        if data is not None:
            self.field_width = data[0]
            for i in xrange(1, data):
                self.items[i-1].__set__(self.items[i-1], data[i])

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
    def G1(self):
        return self._G1.__get__(self, self._G1)

    @G1.setter
    def G1(self, value):
        self._G1.__set__(self._G1, value)

    @property
    def G2(self):
        return self._G2.__get__(self, self._G2)

    @G2.setter
    def G2(self, value):
        self._G2.__set__(self._G2, value)

    @property
    def G3(self):
        return self._G3.__get__(self, self._G3)

    @G3.setter
    def G3(self, value):
        self._G3.__set__(self._G3, value)

    @property
    def ThetaOrMCID(self):
        return self._ThetaOrMCID.__get__(self, self._ThetaOrMCID)

    @ThetaOrMCID.setter
    def ThetaOrMCID(self, value):
        self._ThetaOrMCID.__set__(self._ThetaOrMCID, value)

    @property
    def ZOFFS(self):
        return self._ZOFFS.__get__(self, self._ZOFFS)

    @ZOFFS.setter
    def ZOFFS(self, value):
        self._ZOFFS.__set__(self._ZOFFS, value)

    @property
    def TFLAG(self):
        return self._TFLAG.__get__(self, self._TFLAG)

    @TFLAG.setter
    def TFLAG(self, value):
        self._TFLAG.__set__(self._TFLAG, value)

    @property
    def T1(self):
        return self._T1.__get__(self, self._T1)

    @T1.setter
    def T1(self, value):
        self._T1.__set__(self._T1, value)

    @property
    def T2(self):
        return self._T2.__get__(self, self._T2)

    @T2.setter
    def T2(self, value):
        self._T2.__set__(self._T2, value)

    @property
    def T3(self):
        return self._T3.__get__(self, self._T3)

    @T3.setter
    def T3(self, value):
        self._T3.__set__(self._T3, value)