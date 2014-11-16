__author__ = 'Michael Redmond'

from ...fields import *
from ...base_cards.simple_card import SimpleCard
from .... import cards
import numpy as np
from math import radians, cos, sin


# noinspection PyPep8Naming
class CORD2C(SimpleCard):
    """Defines a cylindrical coordinate system using the coordinates of three points.

    """

    card_name = 'CORD2C'
    category = 'coordinate_systems'

    defaults = [None,  # ID
                0,     # RID
                None,  # A1
                None,  # A2
                None,  # A3
                None,  # B1
                None,  # B2
                None,  # B3
                None,  # C1
                None,  # C2
                None
                ]

    __slots__ = ('CID', 'RID', 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3',
                 '_CID', '_RID', '_A1', '_A2', '_A3', '_B1', '_B2', '_B3', '_C1', '_C2', '_C3', '_v1', '_v2', '_v3')

    def __init__(self, model=None, data=None):
        super(CORD2C, self).__init__(model)

        self._CID = Integer(self, 0, 0, 100000000, True, True)
        self._RID = Integer(self, 1, 0, None, can_be_blank=True)
        self._A1 = Double(self, 2)
        self._A2 = Double(self, 3)
        self._A3 = Double(self, 4)
        self._B1 = Double(self, 5)
        self._B2 = Double(self, 6)
        self._B3 = Double(self, 7)
        self._C1 = Double(self, 8)
        self._C2 = Double(self, 9)
        self._C3 = Double(self, 10)

        self.field_width = 8

        self.items = [self._CID, self._RID, self._A1, self._A2, self._A3, self._B1, self._B2, self._B3,
                      self._C1, self._C2, self._C3]

        self.set_data(data)

        self._v1 = None
        self._v2 = None
        self._v3 = None

        self.calc_vectors()


    @property
    def ID(self):
        return self._CID.value

    def calc_vectors(self):
        self._v3 = np.array([self.B1 - self.A1, self.B2 - self.A2, self.B3 - self.A3])
        self._v3 /= np.sqrt(self._v3.dot(self._v3))

        self._v1 = np.array([self.C1 - self.A1, self.C2 - self.A2, self.C3 - self.A3])
        self._v1 /= np.sqrt(self._v1.dot(self._v1))

        self._v2 = np.cross(self._v3, self._v1)

        self._v1 = np.cross(self._v2, self._v3)

    def to_reference(self, r, theta=None, z=None):
        if type(r) is list:
            theta = r[1]
            z = r[2]
            r = r[0]

        theta = radians(theta)

        x = r*cos(theta)
        y = r*sin(theta)

        p = x*self._v1 + y*self._v2 + z*self._v3

        return [self.A1 + p[0], self.A2 + p[1], self.A3 + p[2]]

    def to_global(self, r, theta=None, z=None):
        xyz = self.to_reference(r, theta, z)

        if self.RID == 0:
            return xyz

        return self.model.coordinate_systems[self.RID].to_global(xyz)


cards['CORD2C'] = CORD2C