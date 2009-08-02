#-*- coding: utf-8 -*-

import random
from classifier import classifier

class genetyk():
    
    def __init__(self,grammar,properites):
        self.grammar = grammar
        self.properties = properites
    
    def ruletSelection(self):
        suma = 0.0
        for x in self.grammar.G:
            for y in self.grammar.G[x]:
                if len(y.right) == 2:
                    y.r1 = suma
                    suma += y.fitness
                    y.r2 = suma
        
        print "suma:"
        print suma
                    
        print "losowa"
        losowa = random.uniform(0,suma)
        print losowa
        
        for x in self.grammar.G:
            for y in self.grammar.G[x]:

                if y.r1< losowa < y.r2:
                    A = classifier(y.right,y.left)

                        
        losowa = random.uniform(0,suma)
        print losowa
        while 1:
            #print "while"
            for x in self.grammar.G:
                for y in self.grammar.G[x]:
                    if y.r1< losowa < y.r2:
                        if y.compare(A)!=3:
                            B = classifier(y.right,y.left)
                            print "znalazlem"
                            return (A,B)
                        else:
                            losowa = random.uniform(0,suma)

            
        return (A,B)

    def randomSelection(self):
        pass
    
    def elitSelection(self):
        pass
    
    def mutation(self, A):
        #tutaj cos glupiego trzeba wymyslic
        print "mutacja"
        #mutacja lewej strony
        if random.random()<self.properties.Pm:
            D = self.grammar.G.keys()
            tmp = random.randint(0,len(D)-1)
            A.left = D[tmp]

        #mutacja prawej strony
        #1
        if random.random()<self.properties.Pm:
            print "!!!!!!!!!!!!!!!!!!!!!!!"
            print A
            D = self.grammar.G.keys()
            tmp = random.randint(0,len(D)-1)
            A.right = D[tmp] + A.right[1:]
            print A
        #2
        if random.random()<self.properties.Pm:
            print "!!!!!!!!!!!!!!!!!!!!!!!"
            print A
            D = self.grammar.G.keys()
            tmp = random.randint(0,len(D)-1)
            A.right = A.right[:1] +D[tmp] 
            print A
    
    def crossing(self,A,B):
        tmp = A.right
        A.right = B.right
        B.right = tmp
        return A, B
    
    def inversion(self,A):
        A.right = A.right[::-1]        
        return A
    
    def updateGrammar(self):
        pass
    
    def updateProperies(self):
        pass
    
    def makeGen(self):
        ''' tutaj bedzie cala akcja wraz z uaktualnieniem gramatyki'''
        #selekcja dwoch klasyfikatorów za pomocą ruletki (kopie juz)
        A,B = self.ruletSelection()
        
        if random.random()< self.properties.Pk:
            print A
            print B
            self.crossing(A,B)
        
        #tutaj mutajca na A
        self.mutation(A)
        #tutaj mutajca na B
        self.mutation(B)
        
        if random.random()< self.properties.Pi:
            self.inversion(A)
            
        if random.random()< self.properties.Pi:
            self.inversion(B)

        print "dodaje:"
        print A
        print B    
        self.grammar.add(A.left,A.right)
        self.grammar.add(B.left,B.right)
            
    