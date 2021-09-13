# -*- coding: utf-8 -*-

from PyQt4 import QtCore,QtGui
import threading
class AnalyzeThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(AnalyzeThread, self).__init__(parent)

    def run(self):
        t = threading.Thread(target=mdds.multi_thread_detect.main, args=(self.source, myCalbFunc))
        t.start()
        t.join()
