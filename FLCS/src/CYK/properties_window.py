# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'properties_window.ui'
#
# Created: Tue Aug 26 11:08:30 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Properties(object):
    def setupUi(self, Properties):
        Properties.setObjectName("Properties")
        Properties.resize(829,601)
        self.lineEdit = QtGui.QLineEdit(Properties)
        self.lineEdit.setGeometry(QtCore.QRect(20,10,451,71))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Properties)
        QtCore.QMetaObject.connectSlotsByName(Properties)

    def retranslateUi(self, Properties):
        Properties.setWindowTitle(QtGui.QApplication.translate("Properties", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("Properties", "hi hey hello", None, QtGui.QApplication.UnicodeUTF8))

