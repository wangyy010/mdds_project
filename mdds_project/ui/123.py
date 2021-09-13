# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyThread(QThread):

    signalForText = pyqtSignal(QString)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
        self.start()

    def run(self):
        import time
        while True:
            time.sleep(1)
            self.signalForText.emit(QTime.currentTime().toString("hh:mm:ss.zzz"))


class MyEdit(QTextEdit):
    def __init__(self, parent=None):
        super(MyEdit, self).__init__(parent)

    def handleDisplay(self, txtToDisplay):
        self.append(txtToDisplay)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    e = MyEdit()
    e.show()
    t = MyThread()
    t.signalForText.connect(e.handleDisplay)
    app.exec_()
