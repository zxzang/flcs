#-*- coding: utf-8 -*-
from PyQt4 import QtCore
from flcs import gramatyka
from testReporter import testReporter
from membership_Funkctions import membershipFunctions
import time
import sys

class funnction_FLSC(QtCore.QThread):
	def __init__(self, parent):
		super(funnction_FLSC, self).__init__(parent)
		self.ui = parent.ui
		self.function = "licz"
		self.testingWords = []
		self.parent = parent
		self.grammar = gramatyka()
		self.raport = testReporter(self)
		self.membership = membershipFunctions(self)
		
	
	def setFunction(self, function):
		self.function = function
	
	def getFuncton(self):
		return self.function
	
	def getGrammar(self):
		return self.grammar
	
	def getParams(self):
		return self.grammar.parametry
	
	def setTestingWords(self, words):
		self.testingWords = words
		
	def getTestingWords(self):
		return self.testingWords
		
	def run(self):
		if self.function == "licz":
			for x in range(0,5):
				print "licze..."
				time.sleep(1)
		elif self.function == "parseKit":
			#self.raport.makePropertiesHeader()
			self.parseKit()
			#self.raport.close()
		elif self.function == "test":
			self.test()
		else:
			print "funkcja w obłudze FLCS jest nie znana"
			return -1
		
	def parseKit(self):
		'''metoda bedzie parsowac jeden zestaw uczący'''
		#robimy kopie zapasową gramatyki:
		good = 0
		bad = 0
		poprawnie = 0
		nie = 0
		self.grammar.makeBackUp()
		self.grammar.allowCover = 1
		#parsowanie zdań:
		self.grammar.allowFulCover = 1
		x =1
		while 1:
			print "liczymy dla:" + self.testingWords[x]
			#tutaj robimy CYK
			result = self.grammar.CYK(self.testingWords[x])
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
			self.grammar.countProfit(result,len(self.testingWords[x])-2,self.testingWords[x][0])
	    
			if result == 1:
				good += 1
			else:
				bad += 1
			    
			if result == int(self.testingWords[x][0]):
				poprawnie += 1
			else:
				nie += 1
			
			x+=1
			
			#self.ui.window_cyk.setText("sparsowane %d, nie sparsowane %d, poprawnie %d nie poprawnie %d wspony"%(good,bad,poprawnie,nie))
			#self.ui.window_cyk.setText("robie se "+str(x))
			
			self.emit(QtCore.SIGNAL('textOnConsole(PyQt_PyObject)'),"sparsowane %d, nie sparsowane %d, poprawnie %d nie poprawnie %d wspony"%(good,bad,poprawnie,nie))
			self.emit(QtCore.SIGNAL('progresBarUpdate(PyQt_PyObject)'),int(100*x/len(self.testingWords)))
			
			if x >= len(self.testingWords):
				break
			#time.sleep(0.2)
		#self.ui.window_cyk.setText("sparsowane %d, nie sparsowane %d, poprawnie %d nie poprawnie %d wspony"%(good,bad,poprawnie,nie))
		self.grammar.countFitness()
		print "licze membership"
		self.membership.countMembership()
		return 0
	
	def test(self):
		print self.parent.filename

	def getFileName(self):
		return self.getFileName()
	
	def getParams(self):
		return self.grammar.parametry
