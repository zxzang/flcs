#-*- coding: utf-8 -*-


import string, random

from properties import properties
from classifier import classifier
from genetyk import genetyk
from membership_Funkctions import membershipOperations

class gramatyka():
    '''klasa zaiwera gramatyke wraz z operacja,i na niej dostepnymi'''


    def __init__(self):
        #tworzenie instncji parametrow
        self.parametry = properties()
        self.allowFulCover = 1
        #Gramatyka w postaci slownika
        #self.G = {"S":[classifier("AB","S"),classifier("AC","S")],"A":[classifier("BA","A"),classifier("a","A")],"B":[classifier("CC","B"),classifier("b","B")],"C":[classifier("AB","C"),classifier("a","C")]}
        self.G = {"S":[classifier("AB","S"),classifier("AC","S")],"C":[classifier("SB","C"),classifier("a","C")],"B":[classifier("BB","B"),classifier("b","B")],"A":[classifier("a","A")]}
        self.G_backUp = {"S":[classifier("AB","S"),classifier("AC","S")],"C":[classifier("SB","C"),classifier("a","C")],"B":[classifier("BB","B"),classifier("b","B")],"A":[classifier("a","A")]}
        self.classifierNum=0
        self.allowCover = 1
        self.membershipCounter = membershipOperations(self)

        for x in self.G:
            for y in self.G[x]:
                if len(y.right)>1:
                    self.classifierNum+=1

    def makeBackUp(self):
        self.G_backUp = self.G

    def bringBackGrammar(self):
        self.G = self.G_backUp

    def CYK(self, slowo):
        ''' algorytm CYK '''
        print "CYK"
        #Do poprawienia:
        #1. rozszezenie algorytmu cyk o warotsc mi
        #2. back tracking
        #3. wykorzystywanie funckji przynaleznosci

        # a zem wymyslil
        # 1. S-> w cos w ostatniej komorce jezeli prowadzi do poprawnego rozwiazania a nie prowadzi do nie poprawnego trza wywalic z gramatyki

        poprawnosc = int(slowo[0])
        slowo = slowo[1:]
        #tymczasowa tablica do klasyfikatorów:
        tmp = []
        self.table_CYK=[]

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
        self.table_CYK.append(tmp)

        #zastosowanie pokrycia startowego przerwanie algorytmu
        #musi nastąpić reset ustawień w metodzie nadrzędnej
        if len(slowo) == 1:
            if self.pokrycieStartowe(slowo[0]) == 1:
                return -10

        #wypelnianie dalszych poziomow:
        wiersz = 1
        pozycja = 0

        while wiersz < len(slowo):
            tmp = []
            while pozycja < (len(slowo)-wiersz):
                pary = self.szukajPar(wiersz,pozycja)
                LL = self.szukajTerminal(pary,self.table_CYK,poprawnosc, wiersz)
                if LL == -10:
                    return -10
                tmp.append(LL)
                pozycja+=1
            self.table_CYK.append(tmp)
            wiersz+=1
            pozycja = 0

        #sprawdzenie poziomu sparsowania zdania:
        #tutaj także bedzie można rozmytość zastosować
        #sprawdzenie czy zdanie sie sparsowalo
        result = 0
        for y in self.table_CYK[len(slowo)-1]:
            for x in y:
                if x == -1:
                    result += 0
                elif x[0].left == 'S':
                    result = 1


        #pokrycie pelne zdanie poprawne i nie sparsowane:
        if poprawnosc == 1 and result == 0 and self.allowFulCover==1:
            if self.pokryciePelne(len(slowo)-1) == 0:
                return -10

        #sprawdzenie poprawnosci cyka
        #if poprawnosc == result:
            #return 1
        #else:
            #return 0
        return result

    def szukajPar(self,a,b):
        '''metoda ta zwraca pary par generujace zdanie dla odpowiedniej pozcycji, pary sa w postacji pozycji w tablicy CYK
        wiersz -> a
        pozycja -> b
        '''
        #print "szukaj par"
        tablica = []
        a=a+1
        b=b+1
        for x in range(1,a):
            tablica.append([[x-1,b-1],[a-x-1,b+x-1]])
        return tablica

    def szukajTerminal(self,K,table_CYK,poprawnosc, wiersz):
        '''metoda zwraca liste pasujacych terminali'''
        #print "szukaj terminali"
        tmp = []
        for x in K:
            for a in table_CYK[x[0][0]][x[0][1]]:
                if a == -1:
                    continue
                for b in table_CYK[x[1][0]][x[1][1]]:
                    if b == -1:
                        continue
                    #do search trzeba przekazac juz odpowiednio zlozona omege:
                    #funkcja przystosowania tutaj wsadzic:
                    wynik=self.search(str(a[0].left)+str(b[0].left),poprawnosc, wiersz)
                    #a i b tutaj sa odpowiednio ojcami nowo wyprowadzonejkomorki, dlatego najpiet liczymy dla tych wartosci unie, nastepnie miksujemy to z nowym klasyfikatorem :):
                    union = self.membershipCounter.countFuzzyUnion(a[1], b[1])
                    if (wynik != -1) and (wynik != -10):
                        for y in wynik:
                            if y != -1:
                                if not y in tmp:
                                    tmp.append((y, self.membershipCounter.countFuzzyUnion(y.omega, union)))
                    elif wynik == -10:
                        return -10
        if len(tmp)<=0:
            tmp = [-1]
        return tmp

    def search(self,terminal,poprawnosc, poziom):
        '''metoda wyszukuje caly slownik w poszukiwaniu klasyfikatorow pasujacych do przekazanego terminalu, rozszerzona o symbol uniwersalny'''
        #print "search"
        find = 0
        result = []

        for x in self.G:
            for T in range(0,len(self.G[x])):
                if ((self.G[x][T].right == terminal) or (self.G[x][T].right == '#')):
                    find = 1
                    #rezygnujemy  z przyznawania poniewaz bedziemy to robic po zakonczeniu rozbioru
                    #self.G[x][T].u[poprawnosc] += 1
                    #tutaj nalezy zastosowac jeszcze funkcje przynaleznosci i ewentualnie odrzuca niepoprawne rozwiazania z gory zakaldajac ze sa zle
                    if poziom == 0:
                        result.append((self.G[x][T],self.G[x][T].omega))
                    else:
                        #tutaj trzeba funkcje uni zastosowac jak to nie jest poziom zerowy:
                        result.append((self.G[x][T]))
                else:
                    pass
                    #możliwość zastosowania logiki rozmytej
                    #uzycie pokrycia agresywnego i restart systemu:
                    #print "agresywne"
                    #if self.parametry.Pa > random.random():
                        #self.pokrycieAgresywne(terminal)

        if find == 1:
            return result
        else:
            if (self.parametry.Pa > random.random()) and (poprawnosc == 1) and (poziom > 1):
                if self.pokrycieAgresywne(terminal) == 1:
                    return -10
            else:
                print "no i nie weszlo w pokrycie agresywne"
        return -1

    def pokrycieTerminalne(self, term):
        '''operacja pokrycia terminalnego, przyjmuje terminal do dodania'''
        print "pokrycie terminalne"
        return self.add(string.upper(term) , term)

    def pokrycieStartowe(self, term):
        '''pokrycie startowe'''
        print "pokrycie startowe"
        return self.add('S',term)

    def pokryciePelne(self, poziom):
        '''FullCover zwraca -1 gdy pokrycie nie jest mozliwe, lub 0 gdy doda terminal taki jak trza'''
        print "pokrycie pelne"
        tab_par=self.szukajPar(poziom,0)

        for x in tab_par:
            for a in self.table_CYK[x[0][0]][x[0][1]]:
                if a == -1:
                    continue
                for b in self.table_CYK[x[1][0]][x[1][1]]:
                    if b == -1:
                        continue
                    self.add('S',str(a[0].left)+str(b[0].left))
                    self.allowFulCover = 0
                    return 0

        return -1

    def pokrycieAgresywne(self, terminal):
        '''i tego tez nie rozumiem
        zorbie tak: ze zbioru detektorow wybieram 3 i robie z nich klasyfikator'''
        print "pokrycie agresywne "+ terminal
        #if self.permisionCover == 0:
            #return 0
        D = self.G.keys()
        tmp = random.randint(0,len(D)-1)
        return self.add(D[tmp],terminal)

    def getGramarStr(self):
        '''metoda zwraca liste klasyfikatorow wraz z ich parametrami w postaci stringa'''
        tmp = ""
        for x in self.G:
            for y in self.G[x]:
                tmp+=y.getClassifierStrExt()
        return tmp

    def getDictionaryStr(self):
        pass


    def add(self, A, B):
        '''dodaje kolejne reguly do gramamtyki A-->B'''
        print "add"
        print self.classifierNum
        tmp=0
        # sprawdzanie czy istnieje juz taki klasyfikator:
        if self.G.has_key(A):
            for x in self.G[A]:
                if x.right==B:
                    #znalazlem juz taki klasyfikator:
                    tmp=1
                    return -1

            if tmp == 0:
                #scisk tutaj:
                if(self.classifierNum >= self.parametry.np):
                    self.scisk(A,B)
                #i dodajemy
                self.G[A].append(classifier(B,A))
                if len(B)>1:
                    self.classifierNum+=1
                print "dodalem"
                print str(A) +'-->' +str(B)

                return 1

            else:
                #print "nie dodalem bo juz jest:)"
                return -1
        else:
            if(self.classifierNum >= self.parametry.np):
                    self.scisk(A,B)
            self.G[A] = [classifier(B,A)]
            print "dodalem"
            print str(A) +'-->' +str(B)
            self.classifierNum+=1
            return 1

    def rem(self,class_rem):
        '''metoda usowa klasyfikator z gramatyki'''
        print "rem"
        i = 0
        for x in self.G[class_rem.left]:
            if x.compare(class_rem) == len(class_rem.right)+1:

                print 'usuwam'
                print self.G[class_rem.left][i]
                self.classifierNum-=1
                del self.G[class_rem.left][i]

                if len(self.G[class_rem.left])==0:
                    del(self.G[class_rem.left])
                print self.classifierNum
                return 1
            i += 1
        print "zem nie usunal !!!!!!!!!!!!!!!!!!!!"
        return 0

    def scisk(self, left, name):
        '''metoda dodaje dany klasyfikator ze sciskiem left-->name'''
        print "scisk"
        cs_table = []
        cf_table = []
        choose = 0
        minmal = 100000

        for y in range(0,self.parametry.cf):
            for x in range(0,self.parametry.cs):
                keys  = self.G.keys()

                while 1:
                    B = random.choice(keys)
                    #if len(self.G[B])>1:
                        #break
                    K = self.G[B][random.randint(0,len(self.G[B])-1)]
                    if len(K.getRight()) > 1:
                        break

                if K.fitness <=  minmal:
                    minmal = K.fitness
                    choose = K

            cf_table.append(K)

        #return cf_table
        #szukamy najbardziej podobnego:
        podobienstwo_max = -1
        tmp_cla = classifier(name,left)
        print tmp_cla
        for x in cf_table:
            podobienstwo = x.compare(tmp_cla)
            if podobienstwo_max < podobienstwo:
                choose = x


        #usuwamy najbardziej podobny z klasyfikatorów:
        #self.rem(choose.left, choose.right)
        #dodaje nowy klasyfikator:
        #self.add(left,name)
        return self.rem(choose)

    def countProfit(self, rozbior, word_len, poprawnosc):
        '''metoda liczy profit uzyskany odczas rozbioru poprawnego/niepoprawnego'''
        print "count profit"

        #sprawdzamy czy rzobior byl napewno do konca zrobiony:
        result = 0
        for y in self.table_CYK[word_len]:
            for x in y:
                if x == -1:
                    pass
                elif x[0].left == 'S':
                    result = 1

        for x in range(0,word_len):
            for y in self.table_CYK[x]:
                for n in y:
                    if n != -1:
                        n[0].u[int(poprawnosc)] += 1
                        if result == 1:
                            if int(poprawnosc) == 1:
                                n[0].p += self.parametry.ba*pow(2,x)*self.parametry.raf
                            else:
                                n[0].d += self.parametry.ba*pow(2,x)*self.parametry.raf
        #if rozbior == 0:
            #for x in self.usedTerminals:
                #x[0].d += self.parametry.ba*pow(2,x[1])*self.parametry.raf
        #else:
            #for x in self.usedTerminals:
                #x[0].p += self.parametry.ba*pow(2,x[1])*self.parametry.ra

    def countFitness(self):
        #przeniesc to do implementacji klasyfikatora!!!
        print "count fitness"
        #Pd jest (maximum,minimum)
        PD = self.getPD()
        fc = ff = 0

        for x in self.G:
            for y in self.G[x]:
                #liczenie ff:
                if(PD[0]-PD[1]!=0.0):
                    ff = (y.p -y.d - PD[1])/(PD[0]-PD[1])
                else:
                    ff = 0.0

                #liczenie fc:
                if((y.u[0]+y.u[1])==0):
                    fc = self.parametry.f0
                else:
                    if (self.parametry.wn*y.u[0]+self.parametry.wp*y.u[1]) != 0:
                        fc = (self.parametry.wp * y.u[1])/(self.parametry.wn*y.u[0]+self.parametry.wp*y.u[1])

                #liczenie przystosowania:
                if (self.parametry.wc + self.parametry.wf) != 0:
                    y.fitness = (self.parametry.wc*fc + self.parametry.wf*ff)/(self.parametry.wc + self.parametry.wf)

    def getPD(self):
        '''metoda zwaraca krorke (max(p-d),min(p-d)) '''
        print "get PD"
        minimum = 0.0
        maximum = 0.0
        for x in self.G:
            for y in self.G[x]:
                tmp = y.p - y.d
                if tmp < minimum:
                    minimum = tmp
                if tmp > maximum:
                    maximum = tmp
        return (maximum,minimum)

    def setParams(self,properties):
        self.parametry = properties

    def getParams(self):
        return self.parametry


#testy:
G = gramatyka()
gen = genetyk(G,G.parametry)
result = -10
while result == -10:
    result = G.CYK('1abba')
tab = G.table_CYK


print "wynik cyka " + str(result)
for x in tab:
    print x
G.countProfit(result,len('1abba')-2,1)
G.countFitness()

print G.getGramarStr()

print "genetyczny przedsawiamy:"
gen.makeGen()
#tmp.right = "dupa"
print G.getGramarStr()


