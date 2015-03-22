__author__ = 'Michael Redmond'


class HDF5Hierarchy(object):
    def __init__(self):
        super(HDF5Hierarchy, self).__init__()

        self._sol_group = None
        self._sort_group = None
        self._table_group = None

        self._sol_groups = ('SOL101', 'SOL106')
        self._table_groups = ('Displacements', 'Grid Point Forces')

    def set_solution_group(self, sol_group):
        if sol_group in self._sol_groups:
            self.sol_group = sol_group
        else:
            self.sol_group = None
            print "Solution type %s is not supported!" % sol_group

    def set_sort_group(self, sort_group):
        if sort_group in ('SORT1', 'SORT2'):
            self._sort_group = sort_group
        else:
            self._sort_group = None
            print "Sort type %s is not supported!" % sort_group

    def set_table_group(self, table_group):
        if table_group in self._table_groups:
            self._table_group = table_group
        else:
            pass
