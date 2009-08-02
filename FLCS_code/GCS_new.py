#-*- coding: utf-8 -*-

import sys, string, random
from CYK_new import gramatyka
from properties import properties
from PyQt4 import QtCore, QtGui
from okno_new import Ui_GCS
from gen_learning import tasks_generator
from genetyk import genetyk


class MyForm(QtGui.QMainWindow):
    #definicja zmiennych :
    word = "1aabb"
    
   
    #G.setProperties(parametry)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
	self.dialogTasks = tasks_generator(self)
        self.ui = Ui_GCS()
	self.parametry = properties()
	self.testingWords = []
        self.ui.setupUi(self)
        self.G = gramatyka()
	self.genetyk = genetyk(self.G,self.parametry)
	self.fileIndex = 0
        #self.ui.window_CYK.addTab(self.genTabCYK())
	print "tutaj gramtyka na okno idzie:"
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
	
	#generowanie zdan uczacych button:
	QtCore.QObject.connect(self.ui.create_test,QtCore.SIGNAL("clicked()"),self.generate_tasks)
	
	#anulowanie wprowadzanych preferenci
	QtCore.QObject.connect(self.ui.propertiesCancel,QtCore.SIGNAL("clicked()"),self.cancelProperties)
	#QtCore.QObject.connect(self.ui.change_word,QtCore.SIGNAL("clicked()"),self.readLine)
	self.cancelProperties()
    
    def genTabCYK(self): 
	''' metoda bedzie odpowiadac za petle główna porgramu'''
	print "w GCS ie"
	#odświerzenie widoku gramatyki:
	self.parsKit()
	print "selekcja ruletkowa:"
	self.genetyk.makeGen()
	self.ui.window_grammar.setText(self.G.getGramarStr())
	print "koniec done!"
	
    
    def readLine(self):
	if self.fileIndex == len(self.testingWords) -1:
	    self.fileIndex = 0
	    self.G.countFitness()
        self.fileIndex += 1
	x=self.fileIndex
	
	self.word = self.testingWords[self.fileIndex]
        self.ui.window_cyk.setText(self.testingWords[self.fileIndex])
	result = self.G.CYK(self.testingWords[self.fileIndex])
	
	if result is int:
	    return 0
	self.G.countProfit(result,len(self.testingWords[x])-1,self.testingWords[x][0])
	self.ui.window_grammar.setText(self.G.getGramarStr())

    def parsKit(self):
	'''metoda bedzie parsowac jeden zestaw uczący'''
	#robimy kopie zapasową gramatyki:
	good = 0
	bad = 0
	poprawnie = 0
	nie = 0
	self.G.makeBackUp()
	self.G.allowCover = 1
	#parsowanie zdań:
	self.G.allowFulCover = 1
	x =1
	while 1:
	    print "liczymy dla:" + self.testingWords[x]
	    #tutaj robimy CYK
	    result = self.G.CYK(self.testingWords[x])
	    if result == -10:
		#przerwanie, reset z powodu zastosowania pokrycia:
		print "reset"
		x = 1
		good = 0
		bad = 0
		poprawnie = 0
		nie = 0
		continue
	    #jak się skończy to liczymy p i d jeszcze czyba u by trzeba bylo:
	    self.G.countProfit(result,len(self.testingWords[x])-2,self.testingWords[x][0])

	    if result == 1:
		good += 1
	    else:
		bad += 1
		
	    if result == int(self.testingWords[x][0]):
		poprawnie += 1
	    else:
		nie += 1
	    
	    x+=1
	    if x >= len(self.testingWords):
		break
	self.ui.window_cyk.setText("sparsowane %d, nie sparsowane %d, poprawnie %d nie poprawnie %d wspony"%(good,bad,poprawnie,nie))
	self.G.countFitness()
	return 0
	    
	
    def showDict(self):
        self.ui.okno_gl.setText(str(self.G.G)) 

    def changeWord(self):
	pass

    def openFile(self):
	''' metoda otwiera wskazany plik, i wyswietla'''
	
	tmp = ''
        fd = QtGui.QFileDialog(self)
	self.filename = fd.getOpenFileName()
	from os.path import isfile
	if isfile(self.filename):
	    for x in open(self.filename):
		self.testingWords.append(x[:len(x)-1])
		
	self.editFile()
	
	for x in self.testingWords:
	    tmp+=x + "\n" #+" len: " + str(len(x)) + "\n"
	self.ui.window_file.setText(tmp)
	
	
    def editFile(self):
	for x in range(0,len(self.testingWords)):
	    #tmp = self.testingWords[x][0]
	    self.testingWords[x] = self.testingWords[x][0]+self.testingWords[x][self.testingWords[x][2:].find(" ")+3:]
	    #usuwanie spacji:
	    while self.testingWords[x].find(" ") > 0:
		k = self.testingWords[x].find(" ")
		self.testingWords[x]=self.testingWords[x][:k]+self.testingWords[x][k+1:]
	    self.testingWords[x]=self.testingWords[x].rstrip()	
	    
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
	self.genetyk.updateProperies(self.G.parametry)
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
	
    def generate_tasks(self):
	print "a se kliklem se"
	self.dialogTasks.show()
	
	
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
    
