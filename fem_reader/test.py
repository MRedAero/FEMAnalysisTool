__author__ = 'Michael Redmond'

from nastran.bdf.reader import BDFReader

bdf = BDFReader()

bdf.read_bdf(r'data\wing.bdf')

grids = bdf.nodes.keys()

for i in xrange(len(grids)):
    print bdf.nodes[grids[i]]
    pass

elements = bdf.elements.keys()

for i in xrange(len(elements)):
    element = bdf.elements[elements[i]]
    #if element.card_name == 'CBEAM':
    print bdf.elements[elements[i]]

properties = bdf.properties.keys()

for i in xrange(len(properties)):
    property = bdf.properties[properties[i]]
    print property


