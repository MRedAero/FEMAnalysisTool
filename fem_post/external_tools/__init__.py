__author__ = 'Michael Redmond'

import sys
import getpass

user = getpass.getuser()

if user == 'Michael':
    # for base_app
    sys.path.append(r'C:/Users/Michael/PycharmProjects/BaseApp7')

    # for fem_utilities
    sys.path.append(r'C:/Users/Michael/PycharmProjects/fem_utilities')

elif user == 'Nick':
    pass