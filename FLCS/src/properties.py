#-*- coding: utf-8 -*-

class properties():
    def __init__(self):
        #krzyzowanie
        self.Pk=0.2
        #mutacja
        self.Pm=0.8
        #inwersja
        self.Pi=0.0
        
        #pelne pokrycie:
        self.Pa=0.0
        self.cf=18
        self.cs=3
        self.ba=1
        self.raf=0.5
        self.ts=0
        #rozmiar populacji:
        self.np=40
        
        self.nstart=0
        self.nN=0
        self.nT=0
        self.nelit=0
        self.nrun=0
        self.nmax=0
        self.wc=1
        self.wf=0
        self.wp=1
        self.wn=2
        self.f0 = 0.5
        
        #zmienne do gui
        self.memebershipFunction = 'none'
        self.fuzzyUnion = 'none'
        self.generalization = 'none'
        
        #zmienne do fuzzy union i conjunction:
        # Yager (0,infinity):
        self.yagerWi = 1.0
        self.yagerWu = 1.0
        #Dubois (0,1):
        self.duboisAlfai = 0.1
        self.duboisAlfau = 0.3
        #Hamacher (0,infinity):
        self.hamacherQi = 1.0
        self.hamacherQu = 1.0
        #Dombi (0, infinity)
        self.dombiWu = 1.0
        self.dombiWi = 1.0
        
        
    def getAtributsString(self):
        tmp = ""
        #krzyzowanie
        tmp += "Pk: " +str(self.Pk) + "\n"
        tmp += "Pm: " +str(self.Pm) + "\n"
        tmp += "Pi: " +str(self.Pi) + "\n"
        tmp += "Pa: " +str(self.Pa) + "\n"
        tmp += "cf: " +str(self.cf) + "\n"
        tmp += "cs: " +str(self.cs) + "\n"
        tmp += "ba: " +str(self.ba) + "\n"
        tmp += "raf: " +str(self.raf) + "\n"
        tmp += "ts: " +str(self.ts) + "\n"
        tmp += "np: " +str(self.np) + "\n"
        tmp += "nstart: " +str(self.nstart) + "\n"       
        tmp += "nN: " +str(self.nN) + "\n"
        tmp += "nT : " +str(self.nT) + "\n"
        tmp += "nstart : " +str(self.nstart) + "\n"
        tmp += "nelit : " +str(self.nelit) + "\n"
        tmp += "nrun: " +str(self.nrun) + "\n"
        tmp += "nmax: " +str(self.nmax) + "\n"
        tmp += "wc: " +str(self.wc) + "\n"
        tmp += "wf: " +str(self.wf) + "\n"
        tmp += "wp: " +str(self.wp) + "\n"
        tmp += "wn: " +str(self.wn) + "\n"
        tmp += "f0: " +str(self.f0) + "\n"
        return tmp
        
        
#mozna oposcic plodnosc, ff nie jest brana pod uwage.