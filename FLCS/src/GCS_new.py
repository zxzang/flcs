#-*- coding: utf-8 -*-

import sys, string, random
from CYK_new import gramatyka
from properties import properties
from PyQt4 import QtCore, QtGui
from okno_new import Ui_GCS
from gen_learning import tasks_generator
from genetyk import genetyk
from thread_flcs import funnction_FLSC
from popUps import popUp


class MyForm(QtGui.QMainWindow):
    #definicja zmiennych :
    word = "1aabb"


    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
    	self.dialogTasks = tasks_generator(self)
        self.ui = Ui_GCS()
    	self.parametry = properties()
    	self.testingWords = []
        self.ui.setupUi(self)
    	self.FLCS = funnction_FLSC(self)
    	#definiuje obiekt obsługujący popUp'y:
    	self.popUp = popUp(self)
    	self.genetyk = genetyk(self.FLCS.getGrammar(),self.parametry)
    	self.fileIndex = 0
        #self.ui.window_CYK.addTab(self.genTabCYK())

        #print "tutaj gramtyka na okno idzie:"
        self.ui.window_grammar.setText(self.FLCS.getGrammar().getGramarStr())

        #dodawanie dotatkowych combosow w oknie:
        self.addMembershipFunctionBox()
        self.addFuzzyFunctionBox()
        #ustawianie polaczen:

    	#wystartowanie algorytmu:
        QtCore.QObject.connect(self.ui.start_GLBS, QtCore.SIGNAL("clicked()"),self.genTabCYK)

    	#otwieranie pliku
        QtCore.QObject.connect(self.ui.menuOpcje, QtCore.SIGNAL("clicked()"),self.openFile)


    	#przycisk do testow (nastepny krok)
        QtCore.QObject.connect(self.ui.change_word,QtCore.SIGNAL("clicked()"),self.testy)

    	#nastepny krok
    	#QtCore.QObject.connect(self.ui.change_word,QtCore.SIGNAL("clicked()"),self.readLine)

    	#pobranie danych z formularza zmiennych
    	QtCore.QObject.connect(self.ui.propertiesAccept,QtCore.SIGNAL("clicked()"),self.getProperties)

    	#generowanie zdan uczacych button:
    	QtCore.QObject.connect(self.ui.create_test,QtCore.SIGNAL("clicked()"),self.generate_tasks)

    	#anulowanie wprowadzanych preferenci
    	QtCore.QObject.connect(self.ui.propertiesCancel,QtCore.SIGNAL("clicked()"),self.cancelProperties)
    	#QtCore.QObject.connect(self.ui.change_word,QtCore.SIGNAL("clicked()"),self.readLine)
    	self.cancelProperties()
    	self.getProperties()

    	#otwieranie pliku:
    	QtCore.QObject.connect(self.ui.open_file, QtCore.SIGNAL("clicked()"),self.openFile)

    def checkData(self):
    	'''funkcja bedzie sprwdzac czy dane  do testow zostaly wczytane'''
    	if len(self.testingWords) < 5:
    	    return 0
    	else:
    	    return 1



    def genTabCYK(self):
    	''' metoda bedzie odpowiadac za petle główna porgramu'''
    	print "w GCS ie"
    	if self.checkData():
    	    self.ui.progressBar.setValue(0)
    	    #odświerzenie widoku gramatyki:
    	    self.FLCS.setFunction("parseKit")
    	    self.FLCS.start()
    	    QtCore.QObject.connect(self.FLCS,QtCore.SIGNAL("textOnConsole(PyQt_PyObject)"), self.textOnConsole)
    	    QtCore.QObject.connect(self.FLCS,QtCore.SIGNAL("progresBarUpdate(PyQt_PyObject)"), self.progresBarUpdate)
    	    QtCore.QObject.connect(self.FLCS,QtCore.SIGNAL("finished()"), self.po_wykonaniu_watku)
    	else:
    	    print "dane testowe nie prawidlowe"
    	    self.popUp.setText("Dane nie zostały wczytane")
    	    self.popUp.show()


    def progresBarUpdate(self, progess):
    	self.ui.progressBar.setValue(progess)

    def textOnConsole(self, napis):
    	''' wyświetla przekazany text na konsole glowna aplikacji'''
    	self.ui.window_cyk.setText(napis)

    def  po_wykonaniu_watku(self):
    	print "selekcja ruletkowa:"
    	self.genetyk.makeGen()
    	self.ui.window_grammar.setText(self.FLCS.getGrammar().getGramarStr())
    	print "koniec done!"

    def readLine(self):
    	if self.fileIndex == len(self.testingWords) -1:
    	    self.fileIndex = 0
    	    self.FLCS.getGrammar().countFitness()
            self.fileIndex += 1
    	x=self.fileIndex

    	self.word = self.testingWords[self.fileIndex]
        self.ui.window_cyk.setText(self.testingWords[self.fileIndex])
    	result = self.FLCS.getGrammar().CYK(self.testingWords[self.fileIndex])

    	if result is int:
    	    return 0
    	self.FLCS.getGrammar().countProfit(result,len(self.testingWords[x])-1,self.testingWords[x][0])
    	self.ui.window_grammar.setText(self.FLCS.getGrammar().getGramarStr())



    def showDict(self):
        self.ui.okno_gl.setText(str(self.FLCS.getGrammar().G))

    def changeWord(self):
	       pass

    def openFile(self):
    	''' metoda otwiera wskazany plik, i wyswietla'''
    	print "jezdem"
    	tmp = ''
        fd = QtGui.QFileDialog(self)
    	self.filename = fd.getOpenFileName()
    	from os.path import isfile
    	if isfile(self.filename):
    	    for x in open(self.filename):
    		          self.testingWords.append(x[:len(x)-1])

    	self.editFile()
    	self.FLCS.setTestingWords(self.testingWords)
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
    	self.FLCS.getParams().ba = self.ui.ba.value()
    	self.FLCS.getParams().cf = self.ui.cf.value()
    	self.FLCS.getParams().cs = self.ui.cs.value()
    	self.FLCS.getParams().nelit = self.ui.nelit.value()
    	self.FLCS.getParams().nmax = self.ui.nmax.value()
    	self.FLCS.getParams().nN = self.ui.nN.value()
    	self.FLCS.getParams().np = self.ui.np.value()
    	self.FLCS.getParams().nrun = self.ui.nrun.value()
    	self.FLCS.getParams().nstart = self.ui.nstart.value()
    	self.FLCS.getParams().nT = self.ui.nT.value()
    	self.FLCS.getParams().Pa = self.ui.Pa.value()
    	self.FLCS.getParams().Pi = self.ui.Pi.value()
    	self.FLCS.getParams().Pk= self.ui.Pk.value()
    	self.FLCS.getParams().Pm= self.ui.Pm.value()
    	self.FLCS.getParams().raf= self.ui.raf.value()
    	self.FLCS.getParams().ts= self.ui.ts.value()
    	self.FLCS.getParams().wc= self.ui.wc.value()
    	self.FLCS.getParams().wf= self.ui.wf.value()
    	self.FLCS.getParams().wn= self.ui.wn.value()
    	self.FLCS.getParams().wp= self.ui.wp.value()
    	self.FLCS.getParams().f0= self.ui.f0.value()

    	#pobieranie danych do rozmycia
    	self.FLCS.getGrammar().parametry.fuzzyUnion = str(self.ui.comboBoxUnion.currentText())
    	self.FLCS.getGrammar().parametry.memebershipFunction = str(self.ui.comboBoxMembership.currentText())
    	#tutaj tak durnie sie nazywa bo tak moze kiedys zmienie
    	self.FLCS.getGrammar().parametry.generalization = self.ui.comboBoxUnion_2.currentText()
    	print self.FLCS.getGrammar().parametry.__dict__
    	print str(self.FLCS.getGrammar().parametry.__dict__['generalization']) == 'kwadrat'
    	print str(self.FLCS.getGrammar().parametry.__dict__['memebershipFunction']) == 'Type S'
    	#self.genetyk.updateProperies(self.FLCS.progressgetGrammar().parametry)
    	#self.ui.okno_gl.setText(str(self.ui.ba))
    	#self.ui.window_cyk.setText(str(self.parametry.ba))


    def cancelProperties(self):
    	'''metoda ma za zadanie przywrocenie starych danych do formularza w przypadku wcisniecia "anuluj"'''
    	self.ui.ba.setValue(self.FLCS.getParams().ba)
    	self.ui.cf.setValue(self.FLCS.getParams().cf)
    	self.ui.cs.setValue(self.FLCS.getParams().cs)
    	self.ui.nelit.setValue(self.FLCS.getParams().nelit)
    	self.ui.nmax.setValue(self.FLCS.getParams().nmax)
    	self.ui.nN.setValue(self.FLCS.getParams().nN)
    	self.ui.np.setValue(self.FLCS.getParams().np)
    	self.ui.nrun.setValue(self.FLCS.getParams().nrun)
    	self.ui.nstart.setValue(self.FLCS.getParams().nstart)
    	self.ui.nT.setValue(self.FLCS.getParams().nT)
    	self.ui.Pa.setValue(self.FLCS.getParams().Pa)
    	self.ui.Pi.setValue(self.FLCS.getParams().Pi)
    	self.ui.Pk.setValue(self.FLCS.getParams().Pk)
    	self.ui.Pm.setValue(self.FLCS.getParams().Pm)
    	self.ui.raf.setValue(self.FLCS.getParams().raf)
    	self.ui.ts.setValue(self.FLCS.getParams().ts)
    	self.ui.wc.setValue(self.FLCS.getParams().wc)
    	self.ui.wf.setValue(self.FLCS.getParams().wf)
    	self.ui.wn.setValue(self.FLCS.getParams().wn)
    	self.ui.wp.setValue(self.FLCS.getParams().wp)
    	self.ui.f0.setValue(self.FLCS.getParams().f0)

    def generate_tasks(self):
        print "a se kliklem se"
        self.dialogTasks.show()

    def testy(self):
    	self.FLCS.setFunction("test")
    	self.FLCS.start()

    def getFileName(self):
    	return self.filename

    def getParams(self):
    	return self.FLCS.getGrammar().parametry

    def getGrammar(self):
    	return self.FLCS.getGrammar()

    def addMembershipFunctionBox(self):
    	''' funkcja bedzie dodawac dodatkowe nazwy funckji przynaleznosci do wyboru'''
    	#self.ui.comboBoxMembership.addItem(QtCore.QString("sraka"))
        pass

    def addFuzzyFunctionBox(self):
        ''' funkcja bedzie dodawac dodatkowe nazwy operacji rozmytych do wyboru'''
        self.ui.comboBoxUnion.addItem(QtCore.QString("Zedeh"))
        self.ui.comboBoxUnion.addItem(QtCore.QString("Yager"))
        self.ui.comboBoxUnion.addItem(QtCore.QString("Dubois"))
        self.ui.comboBoxUnion.addItem(QtCore.QString("Hamacher"))
        self.ui.comboBoxUnion.addItem(QtCore.QString("Dombi"))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

