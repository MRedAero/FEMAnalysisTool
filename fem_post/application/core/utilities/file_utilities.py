__author__ = 'Michael Redmond'

import tables

from fem_utilities.nastran.bdf.h5 import BDFH5Reader
from fem_utilities.nastran.bdf.reader import BDFReader


def open_file(filename):
    if tables.is_pytables_file(filename):
        h5_reader = BDFH5Reader(filename)
    else:
        bdf_reader = BDFReader(filename)
        bdf_reader.read_bdf()
        h5filename = bdf_reader.h5filename
        h5_reader = BDFH5Reader(h5filename)

    return h5_reader

