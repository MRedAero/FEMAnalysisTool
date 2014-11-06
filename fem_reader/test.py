__author__ = 'Michael Redmond'

from nastran.bdf.reader import BDFReader

bdf_reader = BDFReader()

bdf = bdf_reader.read_bdf(r'data\spar.bdf')

grids = bdf.nodes.keys()

for i in xrange(len(grids)):
    print bdf.nodes[grids[i]]
    pass

elements = bdf.elements.keys()

for i in xrange(len(elements)):
    element = bdf.elements[elements[i]]
    #if element.card_name == 'CBEAM':
    print bdf.elements[elements[i]]


