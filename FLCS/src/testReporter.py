#-*- coding: utf-8 -*-

import datetime
import sys, os
from properties import properties
########################################################################
class testReporter:
    """Klasa ma za zadanie raportowanie wyników testow"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        os.chdir('testy')
        self.parent = parent
        try:
            self.fileData = self.parent.getFileName()
        except:
            self.fileData = None
        name = str(self.createFileName())
        self.raport = open(name,'a+')
        #self.createFileName()
        #self.raport.write(self.makePropertiesHeader())		
        
        
    def createFileName(self):
        data = str(datetime.datetime.now())
        data = data[:19]+'.txt'
        data = data.replace(' ','_')
        data = data.replace('-','_')
        data = data.replace(':','_')
        return data
    
    def makePropertiesHeader(self):
        #self.parent.getParams().getAtributsString()
        params = self.parent.getParams()
        dict = params.__dict__
        tmp = ""
        self.addLine(str(self.fileData))
        for x in dict:
            tmp += str(x) +" = "+str(dict[x]) + "/n"
            
        self.addLine(tmp)
        
    def addLine(self, line):
        self.raport.write(line)
    
    def close(self):
        self.raport.close()
    
if __name__ == "__main__":
    #cos = testReporter("assa")
    proper = properties()
    print proper.__dict__
    print open.__doc__
    print 'done'
    
    