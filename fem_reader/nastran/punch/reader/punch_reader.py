__author__ = 'Michael Redmond'

import tables
import os
import gc

from ..table_readers import table_readers


class PunchReader(object):
    def __init__(self, pchfilename):
        super(PunchReader, self).__init__()

        self.pchfilename = None
        self.pchfile = None

        self.h5filename = None
        self.h5file = None

        self.set_pch_filename(pchfilename)

        self.data_lines = None

    def set_pch_filename(self, filename):

        self.pchfilename = filename

        self.h5filename = filename.replace(".pch", ".h5")

    def get_table_reader(self, first):
        skip_i = 0
        data_lines = self.data_lines

        header_data = []

        for i in xrange(first, len(data_lines)):
            if data_lines[i][0] != "$":
                break

            header_data.append(data_lines[i])

            skip_i += 1

        table_reader = None

        for i in xrange(len(table_readers)):
            table_reader_cls = table_readers[i]

            if table_reader_cls.matches_format(header_data):
                table_reader = table_reader_cls(self.h5file, header_data)
                break

        return table_reader, skip_i-1

    def skip_table(self, first):
        skip_i = 0
        data_lines = self.data_lines

        for i in xrange(first, len(data_lines)):
            if data_lines[i] == "" or data_lines[i][0] == "$":
                break

            skip_i += 1

        return skip_i-1

    def read_pch(self):

        try:
            self.h5file = tables.open_file(self.h5filename, mode="w", title="%s" % self.h5filename)
        except Exception:
            print "Unable to create h5 file %s!" % self.h5filename
            return

        try:
            self.pchfile = open(self.pchfilename, "rb")
        except Exception:
            print "Unable to open %s!" % self.pchfilename
            self.pchfilename = None
            self.pchfile = None
            self.h5file.close()
            return

        file_size = float(os.path.getsize(self.pchfilename))

        bytes_to_read = 99999927  # ~100 mb of 81 byte lines
        bytes_read = 0

        skip_i = 0

        try:
            while True:

                fraction = 100.*float(bytes_read)/file_size
                fraction = min(100., fraction)

                print "%6.2f" % fraction + "%"

                bytes_read += bytes_to_read

                # force garbage collection
                data = None
                self.data_lines = None
                data_lines = None
                gc.collect()

                data = self.pchfile.read(bytes_to_read)

                if data == "":
                    # no more data to read
                    break

                self.data_lines = data.split('\n')
                data_lines = self.data_lines

                for i in xrange(len(data_lines)):
                    if skip_i:
                        skip_i -= 1
                        continue

                    if data_lines[i] == "":
                        # blank line
                        continue

                    if data_lines[i][0] == "$":
                        table_reader, skip_i = self.get_table_reader(i)
                        continue

                    if table_reader is None:
                        # skip table
                        skip_i = self.skip_table(i)
                        continue

                    skip_i = table_reader.read_table(i, data_lines)

        finally:
            self.h5file.close()
            self.pchfile.close()