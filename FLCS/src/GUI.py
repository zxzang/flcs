import sys, string
from PyQt4 import QtCore, QtGui
from CYK import gramatyka
from okno import Ui_CYK


class MyForm(QtGui.QMainWindow):
    #definicja zmiennych :
    word = "aaaaabbbbsss"
    G = gramatyka()
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_CYK()
        self.ui.setupUi(self)
        # definiuke wlasne polaczenie slotow:
        #QtCore.QObject.connect(self.ui.button_open,QtCore.SIGNAL("clicked()"), self.file_dialog)
        #dodanie slowa:
        QtCore.QObject.connect(self.ui.dodaj_slowo,QtCore.SIGNAL("clicked()"),self.addWord)
        #generacja tablicy CYK:
        QtCore.QObject.connect(self.ui.generujTabCYK,QtCore.SIGNAL("clicked()"),self.genTabCYK)
        #pokaz slownik:
        QtCore.QObject.connect(self.ui.show_dict,QtCore.SIGNAL("clicked()"),self.showDict)
    
    def addWord(self):
        self.word=self.ui.slowo.toPlainText()
        self.ui.okno_gl.setText(self.word)

    def genTabCYK(self):    
        table = self.G.CYK(str(self.word))  
        tmp = "slowo: \t %s \n"%(self.word)
        for x in table:
            tmp += str(x)+"\n"
        self.ui.okno_gl.setText(tmp)
        
        
    def showDict(self):
        self.ui.okno_gl.setText(str(self.G.G))
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
