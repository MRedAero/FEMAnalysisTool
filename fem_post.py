__author__ = 'Michael Redmond'

from PyQt4 import QtCore

QtCore.Signal = QtCore.pyqtSignal

if __name__ == '__main__':
    from fem_post.fem_post import main
    main()