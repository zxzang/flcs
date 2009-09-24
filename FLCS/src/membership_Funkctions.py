#-*- coding: utf-8 -*

import random

class membershipOperations():
    ''' klassa na podstawie gramatyki i aktualnego stanu srodowiska obliczac bedzie funkcje przynaleznosci dla danego klasyfikatora w danym momenci rozbiou zdania'''
    def __init__(self, parent):
        self.parent = parent
        self.functionType = "random"

    def fullRandom(self):
        ''' totalny random funkcji przynaleznosci'''
        return random.random()

    def zadehUnion(self, a, b):
        return max(a,b)

    def zadehConjunction(self, a, b):
        return min(a,b)

    def yagerUnion(self, a, b):
        wu = self.parent.getParams().yagerWu
        tmp = (a**wu +b**wu)**(1/wu)
        return min(1.0,tmp)

    def yagerConjunction(self, a, b):
        wi = self.parent.getParams().yagerWi
        return 1.0 - min(((1.0-a)**wi + (1.0-b)**wi)**(1.0/wi))

    def duboisUnion(self, a, b):
        alfaI = self.parent.getParams().duboisAlfai
        alfaU = self.parent.getParams().duboisAlfau
        return (a+b - a*b - min(a,b,1.0-alfaU))/max(1.0-a,1.0-b,alfaU)

    def duboisConjunction(self, a, b):
        alfaI = self.parent.getParams().duboisAlfai
        alfaU = self.parent.getParams().duboisAlfau
        return (a*b)/max(a,b,alfaI)

    def hamacherUnion(self, a, b):
        qu = self.parent.getParams().hamacherQu
        return (a+b-(2.0 - qu)*a*b)/(1-(1-qu)*a*b)

    def hamacherConjunction(self, a, b):
        qi = self.parent.getParams().hamacherQi
        return (a*b)/(qi + (1.0 - qi)(a+b+a*b))

    def dombiUnion(self, a, b):
        wu = self.parent.getParams().dombiWu
        return 1.0/((1.0+((1/a)-1)**(-1.0*wu) + ((1.0/a)-1)**(-1.0*wu)))**(-1.0/wi)

    def dombiConjunction(self, a, b):
        wi = self.parent.getParams().dombiWi
        return 1.0/((1.0+((1/a)-1)**(-1.0*wi) + ((1.0/a)-1)**(-1.0*wi)))**(-1.0/wi)


    def countFuzzyUnion(self, a, b):
        '''tutaj bedzie juz liczone unia w zaleznosci od wybranej metody'''
        self.functionType = self.parent.getParams().fuzzyUnion

        if self.functionType == "random" or self.functionType == "none":
            return self.fullRandom()
        elif self.functionType == "Yager":
            return self.yagerUnion(a, b)
        elif self.functionType == "Zedeh":
            return self.zedehUnion(a, b)
        elif self.functionType == "Dubois":
            return self.duboisUnion(a,b)
        elif self.functionType == "Hamcher":
            return self.hamacherUnion(a,b)
        elif self.functionType == "Dombi":
            return self.dombirUnion(a,b)
        else:
            return -99

    def countFuzzyConjunction(self, a, b):
        '''tutaj bedzie juz liczone unia w zaleznosci od wybranej metody'''
        if self.functionType == "random":
            return self.fullRandom()
        elif self.functionType == "Yager":
            return self.yagerConjunction(a, b)
        elif self.functionType == "Zedeh":
            return self.zedehConjunction(a, b)
        elif self.functionType == "Dubois":
            return self.duboisConjunction(a,b)
        elif self.function == "Hamcher":
            return self.hamacherConjunction(a,b)
        elif self.function == "Dombi":
            return self.dombirConjunction(a,b)
        else:
            return -99


    def setFunction(self,function):
        self.functionType = function


class membershipFunctions():
    ''' klasa musi z parenta zczytac parametry przetwarzania i uruchomic odpowiednia funkcje przynaleznosci po kazdym zakonczonym rozkladzie zestawu uczacego'''
    def __init__(self, parent):
        self.parent = parent
        self.getParams()

    def getParams(self):
        '''metoda pobiera parametry od rodzica i odpowiednio je ustwaia'''
        parametry = self.parent.getParams()
        self.memberShipType = str(parametry.memebershipFunction)
        self.generalization = str(parametry.generalization)

    def typeS(self):
        '''funkcja ma za zadanie obliczenie funkcji przynaleznosci dla calej gramatyki'''
        a=b=c=0.0
        gramatyka = self.parent.getGrammar()
        (c,a)=gramatyka.getPD()
        #trzeba sie zastanowic nad zmiana definicji b
        b=(c+a)/2
        for x in gramatyka.G:
            for y in gramatyka.G[x]:
                n = y.p-y.d
                if n <= a:
                    y.omega = 0
                elif  n > a and n <= b:
                    y.omega = 2*((n-a)/(c-a))
                elif n>b and n<=c:
                    y.omega= 1-2*((n-a)/(c-a))
                else:
                    y.omega = 1.0

    def kwadrat(self):
        gramatyka = self.parent.getGrammar()
        for x in gramatyka.G:
            for y in gramatyka.G[x]:
                y.omega = y.omega*y.omega

    def pierwiastek(self):
        for x in gramatyka.G:
            for y in gramatyka.G[x]:
                y.omega = y.omega**0.5

    def countMembership(self):
        self.getParams()
        print self.memberShipType
        if self.memberShipType == 'Type S':
            print "licze type S"
            self.typeS()
        else:
            print 'nie wybrano nic'
        if self.generalization == 'kwadrat':
            self.kwadrat()
        elif self.generalization == 'pierwiastek':
            self.pierwiastek()
        else:
            print "brak generalizacji"






