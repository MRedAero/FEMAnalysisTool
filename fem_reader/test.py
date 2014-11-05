__author__ = 'Michael Redmond'

from nastran.bdf.reader import BDFReader

bdf_reader = BDFReader()

bdf = bdf_reader.read_bdf(r'data\wing.bdf')

grids = bdf.nodes.keys()

for i in xrange(len(grids)):
    print bdf.nodes[grids[i]]

elements = bdf.elements.keys()

for i in xrange(len(elements)):
    print bdf.elements[elements[i]]


