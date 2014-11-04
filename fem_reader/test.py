__author__ = 'Michael Redmond'

from nastran.bdf.geometry.grid_points import *
from nastran.bdf.elements.surface_elements import *

grid = GRID()

grid.ID = 1
grid.CP = 1
grid.X1 = 304.1234567899999999
grid.X2 = -0.00000001234567899875641
grid.X3 = 5.
grid.CD = 6
grid.PS = 6
grid.SEID = 7

grid.field_width = 8

print grid

grid.ID = 2

print grid

quad = CQUAD4()
quad.EID = 1
quad.PID = 2
quad.G1 = 3
quad.G2 = 4
quad.G3 = 5
quad.G4 = 6
quad.ThetaOrMCID = 1.
quad.ZOFFS = -1.
quad.TFLAG = 1
quad.T1 = 0.9
quad.T2 = 0.8
quad.T3 = 0.7
quad.T4 = 0.6

print quad

tri = CTRIA3()
tri.EID = 1
tri.PID = 2
tri.G1 = 3
tri.G2 = 4
tri.G3 = 5
tri.ThetaOrMCID = 1.
tri.ZOFFS = -1.
tri.TFLAG = 1
tri.T1 = 0.9
tri.T2 = 0.8
tri.T3 = 0.7

tri.field_width = 16

print tri