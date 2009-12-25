# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created: Mon Sep  7 11:37:15 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 168)
        self.komunikat = QtGui.QLabel(Dialog)
        self.komunikat.setGeometry(QtCore.QRect(30, 30, 561, 71))
        self.komunikat.setObjectName("komunikat")
        self.buttonOK = QtGui.QPushButton(Dialog)
        self.buttonOK.setGeometry(QtCore.QRect(190, 120, 80, 28))
        self.buttonOK.setObjectName("buttonOK")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.komunikat.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonOK.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))

