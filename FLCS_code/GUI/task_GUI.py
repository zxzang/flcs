# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_generate.ui'
#
# Created: Mon Jul 20 22:22:57 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Anuluj(object):
    def setupUi(self, Anuluj):
        Anuluj.setObjectName("Anuluj")
        Anuluj.resize(352, 206)
        self.button_ok = QtGui.QPushButton(Anuluj)
        self.button_ok.setGeometry(QtCore.QRect(30, 170, 80, 27))
        self.button_ok.setObjectName("button_ok")
        self.button_anuluj = QtGui.QPushButton(Anuluj)
        self.button_anuluj.setGeometry(QtCore.QRect(140, 170, 80, 27))
        self.button_anuluj.setObjectName("button_anuluj")
        self.patter = QtGui.QLineEdit(Anuluj)
        self.patter.setGeometry(QtCore.QRect(20, 30, 271, 21))
        self.patter.setObjectName("patter")
        self.max_lenght = QtGui.QSpinBox(Anuluj)
        self.max_lenght.setGeometry(QtCore.QRect(240, 90, 54, 21))
        self.max_lenght.setObjectName("max_lenght")
        self.min_lenght = QtGui.QSpinBox(Anuluj)
        self.min_lenght.setGeometry(QtCore.QRect(240, 120, 54, 23))
        self.min_lenght.setObjectName("min_lenght")
        self.collection_size = QtGui.QSpinBox(Anuluj)
        self.collection_size.setGeometry(QtCore.QRect(240, 150, 54, 23))
        self.collection_size.setObjectName("collection_size")
        self.label = QtGui.QLabel(Anuluj)
        self.label.setGeometry(QtCore.QRect(20, 10, 281, 21))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Anuluj)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 181, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Anuluj)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 181, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Anuluj)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 181, 21))
        self.label_4.setObjectName("label_4")
        self.label_error = QtGui.QLabel(Anuluj)
        self.label_error.setGeometry(QtCore.QRect(20, 60, 271, 16))
        self.label_error.setObjectName("label_error")

        self.retranslateUi(Anuluj)
        QtCore.QMetaObject.connectSlotsByName(Anuluj)

    def retranslateUi(self, Anuluj):
        Anuluj.setWindowTitle(QtGui.QApplication.translate("Anuluj", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.button_ok.setText(QtGui.QApplication.translate("Anuluj", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.button_anuluj.setText(QtGui.QApplication.translate("Anuluj", "Anuluj", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Anuluj", "Podaj wzór gramatyki w formacie a^n*b^n:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Anuluj", "maksymalna dlugosc zdania:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Anuluj", "minimalna dlugosc zdania:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Anuluj", "ilosc zdan uczacych:", None, QtGui.QApplication.UnicodeUTF8))

