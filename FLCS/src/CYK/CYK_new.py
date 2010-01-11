#-*- coding: utf-8 -*-
#klasa ta reperezentowac bedzie gramatyke
# trzeba zamontowac tutaj funkcje umozliwiajace edycje gramtyki
# narazie bedzie to jedynie statyczna klasa posiadajaca jedna gramtyke na sztywno

import string, random

from properties import properties
from classifier import classifier

class gramatyka():
    '''klasa zaiwera gramatyke wraz z operacja,i na niej dostepnymi'''

    
    def __init__(self):
        #tworzenie instncji parametrow
        self.parametry = properties()
        self.usedTerminals =[]
        #Gramatyka w postaci slownika
        #self.G = {"S":[classifier("AB","S"),classifier("AC","S")],"A":[classifier("BA","A"),classifier("a","A")],"B":[classifier("CC","B"),classifier("b","B")],"C":[classifier("AB","C"),classifier("a","C")]}
        self.G = {"S":[classifier("AB","S"),classifier("AC","S")],"C":[classifier("SB","C"),classifier("a","C")],"B":[classifier("BB","B"),classifier("b","B")],"A":[classifier("a","A")]}
        self.classifierNum=0
        
        for x in self.G:
            for y in self.G[x]:
                if len(y.right)>1:
                    self.classifierNum+=1
                    
    def CYK(self, slowo):
        ''' algorytm CYK '''
        #Do poprawienia:
        #1. ocenienie po zakonczeniu
        #2. przerywanie algorytmu
        #3. tablica cyk na obiektach
        #4. uzycie pokrycia
        #5. symbole uniwersalne
        #6. 
        
        poprawnosc = int(slowo[0])
        slowo = slowo[1:]
        #tymczasowa tablica do klasyfikatorów:
        tmp = []
        table_CYK=[]
        
        #uzupelnianie pierwszego wiersza:
        for x in slowo:
            a = self.search(x,poprawnosc, 0)
            if a == -1:
                if poprawnosc == 1:
                    #rezygnuje z wprowadzania pustych znakow na pierwszym poziomie o ile zdanie jest poprawne                    
                    self.pokrycieTerminalne(x)
                    a = self.search(x,poprawnosc,0)
                    tmp.append(a)
                else:
                    tmp.append([-1]) 
            else:
                tmp.append(a)
        table_CYK.append(tmp)
        
        
        #wypelnianie dalszych poziomow:
        wiersz = 1
        pozycja = 0
                
        while wiersz < len(slowo):  
            tmp = []
            while pozycja < (len(slowo)-wiersz):
                pary = self.szukajPar(wiersz,pozycja)
                LL = self.szukajTerminal(pary,table_CYK,poprawnosc, wiersz)
                if LL == -10:
                    return -10
                tmp.append(LL)
                pozycja+=1                
            table_CYK.append(tmp)
            wiersz+=1
            pozycja = 0
        
        return table_CYK
    
    def szukajPar(self,a,b):
        '''metoda ta zwraca pary par generujace zdanie dla odpowiedniej pozcycji'''
        tablica = []
        a=a+1
        b=b+1
        for x in range(1,a):
            tablica.append([[x-1,b-1],[a-x-1,b+x-1]])
        return tablica
    
    def szukajTerminal(self,K,table_CYK,poprawnosc, wiersz):
        '''metoda zwraca liste pasujacych terminali'''
        tmp = []
        for x in K:
            for a in table_CYK[x[0][0]][x[0][1]]:
                if a == -1:
                    continue
                for b in table_CYK[x[1][0]][x[1][1]]:
                    if b == -1:
                        continue
                    print "szukam dla:"
                    print str(a.left)+str(b.left)
                    wynik=self.search(str(a.left)+str(b.left),poprawnosc, wiersz)
                    print "znalazlem:"
                    print wynik
                    if (wynik != -1) and (wynik != -10):
                        for y in wynik:
                            if y != -1:
                                #if not y in tmp:
                                print "dodaje:"
                                print y.getClassifierStr()
                                tmp.append(y)
                    elif wynik == -10:
                        return -10          
        if len(tmp)<=0:
            tmp = [-1]
        return tmp
    
    def search(self,terminal,poprawnosc, poziom):
        '''metoda wyszukuje caly slownik w poszukiwaniu klasyfikatorow pasujacych do przekazanego terminalu, rozszerzona o symbol uniwersalny'''
        find = 0
        result = []
        
        for x in self.G:
            for T in range(0,len(self.G[x])):
                if ((self.G[x][T].right == terminal) or (self.G[x][T].right == '#')):
                    self.usedTerminals.append((T,poziom))
                    find = 1
                    result.append(self.G[x][T])
                else:
                    pass
                    #możliwość zastosowania logiki rozmytej
                    #uzycie pokrycia agresywnego i restart systemu:
                    #print "agresywne"
                    #if self.parametry.Pa < random.random():
                        #self.pokrycieAgresywne(terminal)

        if find == 1:
            return result    
        else:
            return -1    
        
#testy:
G = gramatyka()
tab = G.CYK('1aabb')

#clas = classifier('A','AC')
#tmp = []
#tmp.extend('aaa')
#tmp.extend(clas)
#print tmp

print tab

str = '['
for x in tab:
    str += '['
    for kol in x:
        str += '['
        for el in kol:
            if el == -1:
                str += '-1'
            else:
                str +=  el.getClassifierStr()
        str += ']'
    str += ']'+"\n"
str += ']'

print str
