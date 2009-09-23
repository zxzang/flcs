#-*- coding: utf-8 -*-

import sys
import string
import re
from PyQt4 import QtCore, QtGui
from task_GUI import Ui_Tasks
from thread_flcs import funnction_FLSC


class tasks_generator(QtGui.QMainWindow):
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.regular_expresion = '^(\D)(\^)(\d)((\*)(\D)(\^)(\d))*$'
        self.ui = Ui_Tasks()
        self.ui.setupUi(self)
        #wzór do generowania zbiorów uczących
        self.pattern = ""
        self.max_len = 0
        self.min_len = 0
        self.collection_size = 0
        
        
        #definiujemy 2 zdarzenia OK i Anuluj:
        #QtCore.QObject.connect(self.ui.button_anuluj, QtCore.SIGNAL("clicked()"),self.close)
        QtCore.QObject.connect(self.ui.button_anuluj, QtCore.SIGNAL("clicked()"),self.watek)
        QtCore.QObject.connect(self.ui.button_ok, QtCore.SIGNAL("clicked()"),self.getContent)

    def watek(self):
        self.licz = funnction_FLSC(self,"licz")
        self.licz.start()
        pass
        
        
    def getContent(self):
        self.pattern = self.ui.patter.text()
        re.search(self.regular_expresion,self.pattern)
        if re.search(self.regular_expresion,self.pattern) == None:
            self.ui.label_error.setText("zly format wzoru !!!")
        else:
            self.max_len = int(self.ui.max_lenght.text())
            self.min_len = int(self.ui.min_lenght.text())
            self.collection_size = int(self.ui.collection_size.text())
            
            print self.max_len
            print self.min_len
            print self.collection_size
            
            self.genTasks()
            
    def genTasks(self):
        self.doColections()
        print self.nonterminals
        print self.nonterminals_power
        #trzeba obmyśleć jeszcze jakoś algorytm generowania tego parszywych zdan uczacych
    
    def checkPattern(self):
        ''' trzeba tutaj wyrażenie regularne zastosowac, ale to w pracy bo chce soprano dzisiaj pogladac'''
        pass

    def doColections(self):
        self.nonterminals = []
        self.nonterminals_power = []
        
        x =0
        while 1:
            if (x+2) > len(self.pattern):
                break
            else:
                self.nonterminals.append(str(self.pattern[x]))
                self.nonterminals_power.append(int(self.pattern[x+2]))
                x+=4
            
        pass
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = tasks_generator(None)
    myapp.show()
    sys.exit(app.exec_())

