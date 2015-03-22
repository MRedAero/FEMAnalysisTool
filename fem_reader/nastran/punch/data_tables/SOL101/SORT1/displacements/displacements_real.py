__author__ = 'Michael Redmond'

import tables

from fem_reader.nastran.punch.table_readers import table_readers


class DisplacementsReal(object):

    class LoadcaseTable(tables.IsDescription):
        title = tables.StringCol(64)
        subtitle = tables.StringCol(64)
        label = tables.StringCol(64)
        subcase_id = tables.StringCol(64)

    class DataTable(tables.IsDescription):
        node_id = tables.UInt32Col()
        coord = tables.StringCol(18)
        disp_x = tables.Float64Col()
        disp_y = tables.Float64Col()
        disp_z = tables.Float64Col()
        rot_x = tables.Float64Col()
        rot_y = tables.Float64Col()
        rot_z = tables.Float64Col()

    @classmethod
    def matches_format(cls, header_data):
        if len(header_data) != 6:
            return False

        if header_data[3][:14] != "$DISPLACEMENTS":
            return False

        if header_data[5][:13] != "$SUBCASE ID =":
            return False

        if header_data[4][:12] != "$REAL OUTPUT":
            return False

        if header_data[0][:10] != "$TITLE   =":
            return False

        if header_data[1][:10] != "$SUBTITLE=":
            return False

        if header_data[2][:10] != "$LABEL   =":
            return False

        return True

    def __init__(self, hf5file, header_data):
        super(DisplacementsReal, self).__init__()

        self.hf5file = hf5file

        self._should_read = False

        title = header_data[0][10:72].strip()
        subtitle = header_data[1][10:72].strip()
        label = header_data[2][10:72].strip()
        subcase_id = header_data[5][13:72].strip()

        NodeError = tables.exceptions.NodeError

        try:
            self.sol_group = self.hf5file.create_group("/", "SOL101", "SOL101 Data")
        except NodeError:
            self.sol_group = self.hf5file.SOL101

        try:
            self.sort_group = self.hf5file.create_group(self.sol_group, "SORT1", "SORT1 Data")
        except NodeError:
            self.sort_group = self.sol_group.SORT1

        try:
            self.data_group = self.hf5file.create_group(self.sort_group, "DisplacementsReal", "Displacements Data")
        except NodeError:
            self.data_group = self.sort_group.DisplacementsReal

        try:
            self.lc_table = self.hf5file.create_table(self.data_group, "Loadcases", self.LoadcaseTable,
                                                      "Loadcase Table Data")
        except NodeError:
            self.lc_table = self.data_group.Loadcases

        subcase_table = "subcase_id_%s" % subcase_id

        try:
            self.data_table = self.hf5file.create_table(self.data_group, subcase_table, self.DataTable,
                                                      "Subcase %s Data" % subcase_id)
        except NodeError:
            self.data_table = getattr(self.data_group, subcase_table)

        self.data_row = self.data_table.row

        lc_data = self.lc_table.row

        lc_data['title'] = title
        lc_data['subtitle'] = subtitle
        lc_data['label'] = label
        lc_data['subcase_id'] = subcase_id
        lc_data.append()
        self.lc_table.flush()

        self.count = 0

        self.finished = False

        self._should_read = True

    def read_table(self, first, data_lines):
        if not self._should_read:
            return 0

        skip_i = 0

        my_int = int
        my_float = float

        for i in xrange(first, len(data_lines)):

            data_line = data_lines[i]

            if data_line == "" or data_line[0] == "$":
                self.finished = True
                break

            skip_i += 1

            if self.count == 0:
                self.data_row['node_id'] = my_int(data_line[:10].strip())
                self.data_row['coord'] = data_line[10:18].strip()
                self.data_row['disp_x'] = my_float(data_line[18:36].strip())
                self.data_row['disp_y'] = my_float(data_line[36:54].strip())
                self.data_row['disp_z'] = my_float(data_line[54:72].strip())
                self.count = 1
            elif self.count == 1:
                self.data_row['rot_x'] = my_float(data_line[18:36].strip())
                self.data_row['rot_y'] = my_float(data_line[36:54].strip())
                self.data_row['rot_z'] = my_float(data_line[54:72].strip())
                self.data_row.append()
                self.count = 0

        self.data_table.flush()

        return skip_i-1


table_readers.append(DisplacementsReal)
