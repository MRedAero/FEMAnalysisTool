__author__ = 'Michael Redmond'

import tables

from fem_utilities.nastran.bdf.bdf_to_h5 import BDFH5
from fem_utilities.nastran.bdf.bdf_to_h5.bdf_reader import BDFReader


def open_file(filename):
    if tables.is_pytables_file(filename):
        h5_reader = BDFH5()
        h5_reader.open_file(filename)
    else:
        bdf_reader = BDFReader(filename)
        bdf_reader.read_bdf()
        h5_reader = bdf_reader.h5file

    return h5_reader

