##klasa ta reperezentowac bedzie gramatyke
# trzeba zamontowac tutaj funkcje umozliwiajace edycje gramtyki
# narazie bedzie to jedynie statyczna klasa posiadajaca jedna gramtyke na sztywno
import string

class gramatyka():
    '''klasa zaiwera gramatyke wraz z operacja,i na niej dostepnymi'''
    def __init__(self):
    #Gramatyka w postaci slownika
    #"S":[classifier("AB"),classifier("AC")],
        #self.G = {"S":[classifier("AB"),classifier("AC")],"A":[classifier("BA"),classifier("a")],"B":[classifier("CC"),classifier("b")],"C":[classifier("AB"),classifier("a")]}
        self.G = {"S":[classifier("AB"),classifier("AC")],"C":[classifier("SB"),classifier("a")],"B":[classifier("BB"),classifier("b")],"A":[classifier("a")]}
    
    def add(self, A, B):
        '''dodaje kolejne reguly do gramamtyki, jeszcze nie przetestowane czy poprawnie dziala,a z obiektowym podejsciem do klasyfikatora to napewno nie'''
        if self.G.has_key(A):    
            self.G[A].append(classifier(B))
        else:
            self.G[A] = [classifier(B)]
            
    def search(self,terminal,poprawnosc):
        '''metoda wyszukuje caly slownik w poszukiwaniu klasyfikatorow pasujacych do przekazanego terminalu, metoda rozszezona o symbol uniwersalny'''
        find = 0
        self.result = []
        for x in self.G:
            for T in self.G[x]:
                if ((T.name == terminal) or (T.name == '#')):
                    find = 1
                    self.result.append(x)
                    T.u[poprawnosc]+=1
        if find == 1:    
            return self.result
        else:
            return -1
    
    def getGramarStr(self):
        tmp = ""
        for x in self.G:
            for y in self.G[x]:
                tmp += str(x) + " -->" + y.name + "\n"
        return tmp    
        
        
    def CYK(self, slowo):
        #flaga poprawnosci rozpatrywanego zdania
        poprawnosc = slowo[0]
        slowo = slowo[1:]
        tmp = []
        table_CYK =[]
        final = []
        #peirwsza czesc odpowiadajaca za wypelnienie pierwszego wiersza w tabeli
        for x in slowo:
            a = self.search(x,poprawnosc)
            if a == -1:
                #tutaj dodawanie do slownika:
                self.add(string.upper(x),x)
                tmp.append([-1])
            else:
                tmp.append(a)
        table_CYK.append([])
        table_CYK[0] = tmp[0:]
        
        #tutaj jakas totalna masakra taka ze glowa mala:):
        #table_CYK.append([])
        poziom=1
        while poziom < (len(table_CYK[0])):
            table_CYK.append([])
            #k jest iteratorem dla while, nic pozatym
            k=0
            while k < len(table_CYK[0])-poziom:
                tmp=[]
                ##tutaj zakres nie jest obknuty do konca
                ##cos - poziom po ktorym aktualnie poszukujemy:
                for cos in range(0,poziom):
                    if cos<=(poziom-1-cos):    
                        for a in table_CYK[cos][k]:
                            if table_CYK[cos][k] == -1:
                                tmp=[]
                            else:                            
                                for b in table_CYK[poziom-1-cos][k+1+cos]:
                                    #print "if: dla [%d;%d] [%d;%d] szukam %s%s"%(cos,k,poziom-1-cos,k+1+cos,str(a),str(b))
                                    wynik = self.search(str(a)+str(b),poprawnosc)
                                    if wynik != -1:
                                        #if (wynik in tmp) == False:
                                        if not [elements in wynik for elements in tmp]:                            
                                            tmp.extend(wynik)
                                            #print "else: dla [%d;%d] [%d;%d]  szukam %s%s"%(cos,k,poziom-1-cos,k+1,str(a),str(b))                                    
                    else:
                        for b in table_CYK[cos][k]:
                            if table_CYK[cos][k] == -1:
                                tmp=[]        
                            for a in table_CYK[poziom-1-cos][k+1+cos]:
                                #print "else: dla [%d;%d] [%d;%d] szukam %s%s"%(cos,k+1,poziom-1-cos,k+1+cos,str(b),str(a))
                                wynik = self.search(str(b)+str(a),poprawnosc)
                                if wynik != -1:
                                    if not [elements in wynik for elements in tmp]:
                                        tmp.extend(wynik)
                                                                    
                if len(tmp) <= 0:
                    tmp = [-1]
                table_CYK[poziom].append(tmp)
                k+=1
            #print "ostatio wygenerowany poziom"
            #print table_CYK[poziom]
            poziom+=1
            
        return table_CYK
        
    def addStartSymbol(self,A):
        tmp = 0
        if self.G.has_key("S"):
            for x in self.G["S"]:
                if x.name == A:
                    tmp+=1        
            if tmp == 0:    
                self.G["S"].append(classifier(A))
                    #tu dodajemy tylko nie wiemy jak
        else:
            #tutaj musimy dodac juz calos wraz z kluczem:) 
            self.G['S']=[classifier(A)]
           

    
    def krzyzowanie(self,A,B):
        pass
        
    def mutacja(self):
        pass
        
    def inwersja(slef):
        pass
##klasa bedzie udawac zachowanie multiplekasera, bede jej uzywac do testow
class classifier():
    '''klasa bedzie representowac klasyfikator w systemie'''
    def __init__(self,name):
        #prawa strona kalsyfikatora
        self.name = name
        #ilosc poprawnych uzyc
        self.u = []
        self.u.append(0)
        #ilosc niepoprawnych uzyc
        self.u.append(0)
        
    def set(self,name):
        self.name=name
    
    

#C = classifier("kupa")
#print C.name
#C.set("aaa")
#print C.name
G = gramatyka()
G.addStartSymbol('g')
#G.add("S","asasa")
for x in G.G['S']:
    print x.name
G.addStartSymbol('c')
for x in G.G['S']:
    print x.name
#K = G.CYK("abaaaaabbaba")
#print "final:"
#for x in K:
#    print x
