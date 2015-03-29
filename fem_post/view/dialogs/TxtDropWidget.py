__author__ = 'NickWilson'


from PyQt4 import QtGui, QtCore

class TxtDrop(QtGui.QTextEdit):
    def __init__(self, type, parent=None):
        super(TxtDrop, self).__init__(parent)
        #super().__init__(parent=parent)

        self.setAcceptDrops(True)
        #self.setIconSize(QtCore.QSize(72, 72))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            drpfile = str(event.mimeData().urls()[0].toLocalFile())

            self.emit(QtCore.SIGNAL("dropped"), drpfile)
        else:
            event.ignore()

