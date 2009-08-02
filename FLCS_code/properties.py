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
        
#mozna oposcic plodnosc, ff nie jest brana pod uwage.