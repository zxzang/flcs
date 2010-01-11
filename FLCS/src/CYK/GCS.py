import sys, string
from CYK import gramatyka
from properties import properties
from PyQt4 import QtCore, QtGui
from okno_new import Ui_GCS

class MyForm(QtGui.QMainWindow):
    #definicja zmiennych :
    testingWords = []
    fileIndex = 0
    word = "aabb"
    G = gramatyka()
    parametry = properties()
    #G.setProperties(parametry)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_GCS()
        self.ui.setupUi(self)
        
        #self.ui.window_CYK.addTab(self.genTabCYK())
        self.ui.window_grammar.setText(self.G.getGramarStr())
	
        #ustawianie polaczen:
	
	#wystartowanie algorytmu:
        QtCore.QObject.connect(self.ui.start_GLBS, QtCore.SIGNAL("clicked()"),self.genTabCYK)
	
	#otwieranie pliku
        QtCore.QObject.connect(self.ui.menuOpcje, QtCore.SIGNAL("clicked()"),self.openFile)
	
	#puusty przycis narazie
        #QtCore.QObject.connect(self.ui.change_word,QtCore.SIGNAL("clicked()"),self.changeWord) 
	
	#otwieranie pliku:
	QtCore.QObject.connect(self.ui.open_file, QtCore.SIGNAL("clicked()"),self.openFile)
	
	#nastepny krok
	QtCore.QObject.connect(self.ui.change_word,QtCore.SIGNAL("clicked()"),self.readLine)
	
	#popranie danych z formularza zmiennych, jeszcze sa tam jakies braki!!
	QtCore.QObject.connect(self.ui.propertiesAccept,QtCore.SIGNAL("clicked()"),self.getProperties)
	
	#anulowanie wprowadzanych preferenci
	QtCore.QObject.connect(self.ui.propertiesCancel,QtCore.SIGNAL("clicked()"),self.cancelProperties)
	#QtCore.QObject.connect(self.ui.change_word,QtCore.SIGNAL("clicked()"),self.readLine)
	self.cancelProperties()
    
    def genTabCYK(self): 
	
	print "w GCS ie"
	print self.word
        table = self.G.CYK(str(self.word))  
	while table == 0:
	    table = self.G.CYK(str(self.word))

	if table == -10:
	    print "sdffffffffffffffffffffffff"
	    return -10
	tmp = ""
        for x in table:
            tmp += str(x)+"\n"
        self.ui.window_cyk.setText(tmp)
	self.ui.window_grammar.setText(self.G.getGramarStr())
    
    def readLine(self):
	if self.fileIndex == len(self.testingWords) -1:
	    self.fileIndex = 0  
        self.fileIndex += 1
	self.word = self.testingWords[self.fileIndex]
        self.ui.window_cyk.setText(self.testingWords[self.fileIndex])
	self.genTabCYK()
	
    def showDict(self):
        self.ui.okno_gl.setText(str(self.G.G)) 

    def changeWord(self):
	pass

    def openFile(self):
	''' metoda otwiera wskazany plik, i wyswietla'''
	#co dalej z tym tekstem dlaczego ich ....
	tmp = ''
        fd = QtGui.QFileDialog(self)
	self.filename = fd.getOpenFileName()
	from os.path import isfile
	if isfile(self.filename):
	    for x in open(self.filename):
		self.testingWords.append(x[:len(x)-1])
	self.editFile()
	for x in self.testingWords:
	    tmp+=x  #+" len: " + str(len(x)) + "\n"
	self.ui.window_file.setText(tmp)
	
	
    def editFile(self):
	for x in range(0,len(self.testingWords)):
	    #tmp = self.testingWords[x][0]
	    self.testingWords[x] =self.testingWords[x][0]+self.testingWords[x][self.testingWords[x][2:].find(" ")+3:]
	    while self.testingWords[x].find(" ") > 0:
		k = self.testingWords[x].find(" ")
		self.testingWords[x]=self.testingWords[x][:k]+self.testingWords[x][k+1:]
	
    def getProperties(self):
	'''metoda ma za zadanie zczytywanie zmiennych, ale nie wiem jak z qwidegta pobrac dane'''
	self.G.parametry.ba = self.ui.ba.value()
	self.G.parametry.cf = self.ui.cf.value()
	self.G.parametry.cs = self.ui.cs.value()
	self.G.parametry.nelit = self.ui.nelit.value()
	self.G.parametry.nmax = self.ui.nmax.value()
	self.G.parametry.nN = self.ui.nN.value()
	self.G.parametry.np = self.ui.np.value()
	self.G.parametry.nrun = self.ui.nrun.value()
	self.G.parametry.nstart = self.ui.nstart.value()
	self.G.parametry.nT = self.ui.nT.value()
	self.G.parametry.Pa = self.ui.Pa.value()
	self.G.parametry.Pi = self.ui.Pi.value()
	self.G.parametry.Pk= self.ui.Pk.value()
	self.G.parametry.Pm= self.ui.Pm.value()
	self.G.parametry.raf= self.ui.raf.value()
	self.G.parametry.ts= self.ui.ts.value()
	self.G.parametry.wc= self.ui.wc.value()
	self.G.parametry.wf= self.ui.wf.value()
	self.G.parametry.wn= self.ui.wn.value()
	self.G.parametry.wp= self.ui.wp.value()
	self.G.parametry.f0= self.ui.f0.value()
	#self.ui.okno_gl.setText(str(self.ui.ba))
	#self.ui.window_cyk.setText(str(self.parametry.ba))
    
    def cancelProperties(self):
	'''metoda ma za zadanie przywrocenie starych danych do formularza w przypadku wcisniecia "anuluj"'''
	self.ui.ba.setValue(self.G.parametry.ba)
	self.ui.cf.setValue(self.G.parametry.cf)
	self.ui.cs.setValue(self.G.parametry.cs)
	self.ui.nelit.setValue(self.G.parametry.nelit)
	self.ui.nmax.setValue(self.G.parametry.nmax)
	self.ui.nN.setValue(self.G.parametry.nN)
	self.ui.np.setValue(self.G.parametry.np)
	self.ui.nrun.setValue(self.G.parametry.nrun)
	self.ui.nstart.setValue(self.G.parametry.nstart)
	self.ui.nT.setValue(self.G.parametry.nT)
	self.ui.Pa.setValue(self.G.parametry.Pa)
	self.ui.Pi.setValue(self.G.parametry.Pi)
	self.ui.Pk.setValue(self.G.parametry.Pk)
	self.ui.Pm.setValue(self.G.parametry.Pm)
	self.ui.raf.setValue(self.G.parametry.raf)
	self.ui.ts.setValue(self.G.parametry.ts)
	self.ui.wc.setValue(self.G.parametry.wc)
	self.ui.wf.setValue(self.G.parametry.wf)
	self.ui.wn.setValue(self.G.parametry.wn)
	self.ui.wp.setValue(self.G.parametry.wp)
	self.ui.f0.setValue(self.G.parametry.f0)
	
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
    
