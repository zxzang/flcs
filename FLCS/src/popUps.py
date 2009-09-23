#-*- coding: utf-8 -*-

from popupWindow import Ui_Dialog
from PyQt4 import QtCore, QtGui


class popUp(QtGui.QMainWindow):
    def __init__(self,parent):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.buttonOK, QtCore.SIGNAL("clicked()"), self.close)
        
    def setText(self,text):
        self.ui.komunikat.setText(QtGui.QApplication.translate("Dialog", text, None, QtGui.QApplication.UnicodeUTF8))