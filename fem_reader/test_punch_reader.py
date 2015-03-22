__author__ = 'Michael Redmond'

from nastran.punch import PunchReader

if __name__ == '__main__':
    reader = PunchReader(r"C:\Users\Michael\Desktop\fem_results\wing_punchandpost.pch")
    reader.read_pch()


