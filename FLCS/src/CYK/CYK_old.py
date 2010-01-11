##klasa ta reperezentowac bedzie gramatyke
# trzeba zamontowac tutaj funkcje umozliwiajace edycje gramtyki
# narazie bedzie to jedynie statyczna klasa posiadajaca jedna gramtyke na sztywno
import string, random

from properties import properties
from classifier import classifier

class gramatyka():
    '''klasa zaiwera gramatyke wraz z operacja,i na niej dostepnymi'''

    
    def __init__(self):
        self.parametry = properties()
        self.usedTerminals =[]
        #Gramatyka w postaci slownika
        #self.G = {"S":[classifier("AB","S"),classifier("AC","S")],"A":[classifier("BA","A"),classifier("a","A")],"B":[classifier("CC","B"),classifier("b","B")],"C":[classifier("AB","C"),classifier("a","C")]}
        self.G = {"S":[classifier("AB","S"),classifier("AC","S")],"C":[classifier("SB","C"),classifier("a","C")],"B":[classifier("BB","B"),classifier("b","B")],"A":[classifier("a","A")]}
        self.classifierNum=0
        
        for x in self.G:
            for y in self.G[x]:
                if len(y.name)>1:
                    self.classifierNum+=1
    
    def setProperties(self,p):
        ''' metoda uaktualnia parametry danego badania'''
        self.parametry=p
                
    def add(self, A, B):
        '''dodaje kolejne reguly do gramamtyki A-->B'''
        tmp=0
        # sprawdzanie czy istnieje juz taki klasyfikator:
        if self.G.has_key(A):
            for x in self.G[A]:
                if x.name==B:
                    tmp=1
                    
            if tmp == 0:
                #scisk tutaj:
                if(self.classifierNum >= self.parametry.np):
                    self.scisk_new(B,A)
                #i dodajemy
                self.G[A].append(classifier(B,A))
                print "dodalem:" + A +"-->"+B
                if len(B)>1:
                    self.classifierNum+=1
                return 1
            
            else:                
                #print "nie dodalem bo juz jest:)"
                return -1
        else:
            if(self.classifierNum >= self.parametry.np):
                    self.scisk_new(B,A)
            self.G[A] = [classifier(B,A)]
            print "dodalem:" + A +"-->"+B
            self.classifierNum+=1
            return 1
            
    def rem(self,A,B):
        '''metoda usowa klasyfikator z gramatyki'''
        tmp = 0
        for x in self.G[A]:
            if x.name == B:
                del self.G[A][tmp]
                self.classifierNum-=1
                return 1
                #print "usuwam"
            tmp+=1
        if len(self.G[A])==0:
            del(self.G[A])
            return 1
        
    def search(self,terminal,poprawnosc, poziom):
        '''metoda wyszukuje caly slownik w poszukiwaniu klasyfikatorow pasujacych do przekazanego terminalu, rozszerzona o symbol uniwersalny'''
        find = 0
        self.result = []
        for x in self.G:
            for T in self.G[x]:
                if ((T.name == terminal) or (T.name == '#')):
                    self.usedTerminals.append((T,poziom))
                    find = 1
                    self.result.append(x)
                    #Tutaj T dodajemy do listy uzytych podaczas parsowania
                    
                    #przyznawanie punktow:
                    T.u[int(poprawnosc)]+=1
                else:
                    #uzycie pokrycia agresywnego i restart systemu:
                    if self.parametry.Pa < random.random():
                        self.pokrycieAgresywne(terminal)
                        #info do systemu ze trzeba restart walnac
                        #return -10
                        
                        #trzeba jeszcze tutaj przerwac

        if find == 1:    
            return self.result    
        else:
            return -1
    
    def getGramarStr(self):
        '''metoda zwraca liste klasyfikatorow wraz z ich parametrami w postaci stringa'''
        tmp = ""
        for x in self.G:
            for y in self.G[x]:
                tmp += str(x) + " -->" + y.name +"\t"+"un= "+str(y.u[0])+"\t"+"up="+str(y.u[1])+"\t fitnes"+str(y.fitness)+ "  p i d  "+"("+str(y.p)+","+str(y.d)+")"+"\n"
        return tmp    
        
        
    def CYK(self, slowo):
        ''' algorytm CYK '''
        succes = 0
        poprawnosc = int(slowo[0])
        slowo = slowo[1:]
        table_CYK=[]
        tmp = []
        used_clas = []
        
        #wypelnianie pierwszego poziomu:
        for x in slowo:
            a = self.search(x,poprawnosc, 0)
            if a == -1:
                if poprawnosc == 1:
                    #rezygnuje z wprowadzania pustych znakow na pierwszym poziomie o ile zdanie jest poprawne                    
                    self.pokrycieTerminalne(x)
                    a = self.search(x,poprawnosc,poprawnosc)
                    tmp.append(a)
                else:
                    tmp.append([-1]) 
            else:
                tmp.append(a)
                
        #pokrycie startowe:
        print "dlugosc="+str(len(slowo))+"  poprawnosc="+str(poprawnosc) + "slowo " +str(slowo)
        
        if (len(slowo)>= 1) and (poprawnosc== 1) and (len(slowo)<= 2):
            print "pokrycie startowe"  
            if self.pokrycieStartowe(slowo) > 0:
                #przerywamy dzialanie algorytmu, poniewaz dodano nowy klasyfikator, nalezy obsluzyc w metodzie nadrzednej
                return 0
            
        table_CYK.append(tmp)
        
        #wywolanie pokrycia agresywnego
        #if (poprawnosc ==1)and (random.random() > self.parametry.Pa):       
                #print "pokrycie agresywne"
                #self.pokrycieAgresywne()
        
        #wypelnianie dalszych poziomow:
        wiersz = 1
        pozycja = 0
                
        while wiersz < len(slowo):  
            tmp = []
            while pozycja < (len(slowo)-wiersz):
                K = self.szukajPar(wiersz,pozycja)
                LL = self.szukajTerminal(K,table_CYK,poprawnosc, wiersz)
                if LL == -10:
                    return -10
                tmp.append(LL)
                pozycja+=1                
            table_CYK.append(tmp)
            wiersz+=1
            pozycja = 0
                
        for x in table_CYK[len(slowo)-1][0]:
            print x
            if x == 'S':
                succes = 1
            if succes == poprawnosc:
                succes = 1
                print "succes"
            else:
                succes = 0
               
        
        self.countProfi(succes)
        if succes != 1:
            #tutaj albo robimy S-> w cos co juz jest w ostatniej komorce, lub trzeba ostatnia komorke wypelnic jeszcze raz i dodac jednego S
            # moze miec postac tylko nie terminalna
            #K = self.szukajPar(len(slowo),0)
            #losujemy jedna z par i dodajemy
            #x = random.randint(0,len(K))
            #lewa = self.szukajTerminal(x,table_CYK,poprawnosc, wiersz)
            #dodac i zreserowac
            #return -1
            pass
        #obbliczenie funkcji przystosowania:
        self.countFitness()

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
                for b in table_CYK[x[1][0]][x[1][1]]:
                    wynik=self.search(str(a)+str(b),poprawnosc, wiersz)
                    if (wynik != -1) and (wynik != -10):
                        for y in wynik:
                            if y != -1:
                                if not y in tmp:
                                    tmp.extend(y)
                    elif wynik == -10:
                        return -10
        if len(tmp)<=0:
            tmp = [-1]
        return tmp
    
    def countFitness(self):
        #przeniesc to do implementacji klasyfikatora!!!
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
        minimum = 0.0
        maximum = 0.0
        for x in self.G:
            for y in self.G[x]:
                tmp = y.p - y.d
                if tmp > minimum:
                    minimum = tmp
                if tmp < maximum:
                    maximum = tmp
        return (maximum,minimum)
                
    def countProfi(self, rozbior):
        if rozbior == 0:
            for x in self.usedTerminals:            
                x[0].d += self.parametry.ba*pow(2,x[1])*self.parametry.raf
        else:
            for x in self.usedTerminals:            
                x[0].p += self.parametry.ba*pow(2,x[1])*self.parametry.raf
        
           
    def universalCover(self):
        '''tutaj nie rozumie do konca idei tego pokrycia'''
        pass
    
    def pokryciePelne(self):
        '''tego tez nie dokonca czaje i trzeba sie zapyac'''
        pass
    
    def pokrycieTerminalne(self, term):
        '''operacja pokrycia terminalnego, przyjmuje terminal do dodania'''
        self.add(string.upper(term) , term)
  
    
    def pokrycieStartowe(self, term):
        '''dodanie pokrycia startowego dal zdan dlugosci 1'''
        return self.add("S" , term)
    
    def pokrycieAgresywne(self, name):
        '''i tego tez nie rozumiem
        zorbie tak: ze zbioru detektorow wybieram 3 i robie z nich klasyfikator'''
        #print "pokrycie agresywne"
        D = self.G.keys()
        tmp = random.randint(0,len(D)-1)
        self.add(D[tmp] ,name)
    
    def krzyzowanie(self,A,B, classA, classB):
        '''metoda krzyzowania klasyfikatoprow, jeszcze nie przetestowana
        nie sprawdzone czy napewno dziala poprawnie!!!'''
        '''tmp=0
        for x in self.G[A]:
            if x.name == classB:
                tmp=1
            if tmp==0:
                self.G[A].append(classifier(classB))
        
        tmp=0
        for x in self.G[B]:
            if x.name == classA:
                tmp=1
            if tmp==0:
                self.G[B].append(classifier(classA))'''
        self.add(A,classB)
        self.add(B,classA)
        
    def mutacja(self):
        '''musze tutaj jeszcze przeimplemntowac inne elementy, dodac tablice terminali(G.keys()) i nieterminali
        nie sprawdzone czy napewno dziala poprawnie!!!'''
        
    def inwersja(self,A,classA):
        ''' genetyk inwersji
        nie sprawdzone czy napewno dziala poprawnie!!!'''
        for x in G[A]:
            if x.name == classB.name:
                tmp=1
            if tmp==0:
                slef.G[A].append(classifier(str(classA[1])+str(classA[0])))
        

    
    def scisk_new(self, left, name):
        '''metoda dodaje dany klasyfikator ze sciskiem left-->name'''
        cs_table = []
        cf_table = []
        choose = 0
        minmal = 100000
        for y in range(0,self.parametry.cf):
            for x in range(0,self.parametry.cs):
                keys  = self.G.keys()
                
                while 1:
                    B = random.choice(keys)
                    if len(self.G[B])>1:
                        break
                while 1:    
                    K = self.G[B][random.randint(0,len(self.G[B])-1)]
                    if len(K.name) > 1:
                        break
                if K.fitness <=  minmal:
                    minmal = K.fitness
                    choose = K
            cf_table.append(K)
        
        #szukamy najbardziej podobnego:
        podobienstwo_max = 0
        for x in cf_table:
            podobienstwo = 0
            if len(name) == 0:
                if x.left == left:
                    podobienstwo += 1
                if x.name[0] == name[0]: 
                    podobienstwo += 1
                if x.name[1] == name[1]: 
                    podobienstwo += 1    
                if podobienstwo > podobienstwo_max:
                    podobienstwo_max = podobienstwo
                    K = x
         
        return self.rem(K.left,K.name)          
        
        
        
#SEKCJA TESTOWA:
G = gramatyka()
print G.getGramarStr()

A = G.CYK("1aa")
while A == 0:
    A = G.CYK("1aabb")

print A
for x in A:
    print x
#A = G.CYK("1h")
#while A == 0:
    #A = G.CYK("1h")
    
print G.getGramarStr()

print "scisk"
#print G.scisk_new()
#B = G.usedTerminals
#for x in B:
    #print x[0].left + "-->"+x[0].name + " poziom: "+str(x[1])
    

#G.countFitness
#print G.scisk_new("A")
#print G.CYK("1a")
#print G.getGramarStr()

#M = G.scisk()
#print G.getGramarStr()
#print M


