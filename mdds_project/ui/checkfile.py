# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checkfile.ui'
#
# Created: Fri Jun 01 17:12:26 2018
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setEnabled(True)
        Form.resize(739, 530)
        Form.setAcceptDrops(False)
        self.fileButton = QtGui.QPushButton(Form)
        self.fileButton.setGeometry(QtCore.QRect(150, 60, 75, 23))
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(60, 20, 541, 20))
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setFrame(False)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.tableView = QtGui.QTableView(Form)
        self.tableView.setGeometry(QtCore.QRect(50, 100, 661, 371))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        '''
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(200, 520, 321, 41))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        '''
        self.startButton = QtGui.QPushButton(Form)
        self.startButton.setGeometry(QtCore.QRect(620, 20, 91, 23))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.directoryButton = QtGui.QPushButton(Form)
        self.directoryButton.setGeometry(QtCore.QRect(340, 60, 75, 23))
        self.directoryButton.setObjectName(_fromUtf8("directoryButton"))
        self.resultButton = QtGui.QPushButton(Form)
        self.resultButton.setGeometry(QtCore.QRect(630, 480, 81, 31))
        self.resultButton.setObjectName(_fromUtf8("resultButton"))
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(600, 60, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.progressLable = QtGui.QLabel(Form)
        self.progressLable.setGeometry(QtCore.QRect(440, 70, 75, 23))
        self.progressLable.setObjectName(_fromUtf8("progressLable"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "恶意文档检查工具", None))
        Form.setWindowIcon(QIcon('icon.png'))
        self.fileButton.setText(_translate("Form", "选择文件", None))
        '''
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600; color:#0000ff;\">恶意文档检查工具</span></p></body></html>", None))
'''
        self.startButton.setText(_translate("Form", "开始检测", None))
        self.directoryButton.setText(_translate("Form", "选择文件夹", None))
        self.resultButton.setText(_translate("Form", "保存结果", None))
        self.tableView_set()

        self.progressLable.setText(_translate("Form", "0 / 0", None))



    def tableView_set(self):
        # 添加表头：
        self.model = QtGui.QStandardItemModel(self.tableView)

        # 设置表格属性：
        self.model.setRowCount(50)
        self.model.setColumnCount(4)

        # 设置表头
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, _fromUtf8(u"文件名"))
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, _fromUtf8(u"文件类型"))
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, _fromUtf8(u"是否为恶意文档"))
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, _fromUtf8(u"描述"))
        self.model.setItem(1, 1, QtGui.QStandardItem('111'))
        self.tableView.setModel(self.model)

        # 设置列宽
        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 80)
        self.tableView.setColumnWidth(2, 100)
        self.tableView.setColumnWidth(3, 500)

        # 合并单元格的效果
        # 第一个参数：要改变的单元格行数
        # 第二个参数：要改变的单元格列数
        # 第三个参数：需要合并的行数
        # 第四个参数：需要合并的列数
        #self.tableView.setSpan(0, 2, 17, 1)
        #self.tableView.setSpan(0, 5, 17, 1)


        # 设置单元格禁止更改
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        # 表头信息显示居中
        self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        #添加表项
        self.tableView.horizontalHeader().setStretchLastSection(True)

