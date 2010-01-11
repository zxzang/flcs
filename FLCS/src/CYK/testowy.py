##klasa ta reperezentowac bedzie gramatyke
# trzeba zamontowac tutaj funkcje umozliwiajace edycje gramtyki
# narazie bedzie to jedynie statyczna klasa posiadajaca jedna gramtyke na sztywno

class gramatyka():
    '''klasa zaiwera gramatyke wraz z operacja,i na niej dostepnymi'''
    def __init__(self):
    #Gramatyka w postaci slownika
        self.Gg = {"S":["AB","BC"],"A":["BA","a"],"B":["CC","b"],"C":["AB","a"]}
        self.G = {"S":["AB","AC"],"C":["SB","a"],"B":["BB","b"],"A":["a"]}
    
    def add(self, A, B):
        '''doaje kolejne reguly do gramamtyki, jeszcze nie przetestowane czy poprawnie dziala'''
        if self.G.has_key(A):    
            self.G[A].append(B)
        else:
            self.G[A] = [B]
            
    def search(self,terminal):
        '''metoda wyszukuje caly slownik w poszukiwaniu klasyfikatorow pasujacych do przekazanego terminalu, metoda rozszezona o symbol uniwersalny'''
        find = 0
        self.result = []
        for x in self.G:
            for T in self.G[x]:
                if ((T == terminal) or (T == '#')):
                  find = 1
                  self.result.append(x)  
        if find == 1:    
            return self.result
        else:
            return -1
    
    def getGramarStr(self):
        tmp = ""
        for x in self.G:
            tmp += str(x) + "-->" + str(self.G[x])+ "\n"
        return tmp    
        
        
    def CYK(self, slowo):
        table_CYK=[]
        tmp = []
        #wypelnianie pierwszego poziomu:
        for x in slowo:
            a = self.search(x)
            if a == -1:
                tmp.append([-1])
            else:
                tmp.append(a)
        
        table_CYK.append(tmp)
        
        wiersz = 1
        pozycja = 0
        while wiersz < len(slowo):
            
            tmp = []
            while pozycja < (len(slowo)-wiersz):
                print "aktualne pole: "+str(wiersz)+str(pozycja)
                #tutaj teraz trzeba odpalic uzupelnianie tablicy:(zamiast print)
                K = self.szukajPar(wiersz,pozycja)
                print "wyszukiwane pary"+str(K)
                tmp.append(self.szukajTerminal(K,table_CYK))
            
                                    
                #print str(table_CYK[x[0][0]][x[0][1]]) + str(table_CYK[x[1][0]][x[1][1]])
                #print "cala linia" + str(M)
                pozycja+=1
            table_CYK.append(tmp)
            wiersz+=1
            pozycja = 0
            print("\n")
        return table_CYK
        
    def szukajPar(self,a,b):
        '''metoda ta zwraca pary par generujace zdanie dla odpowiedniej pozcycji'''
        tablica = []
        a=a+1
        b=b+1
        for x in range(1,a):
            tablica.append([[x-1,b-1],[a-x-1,b+x-1]])
        return tablica
    
    def szukajTerminal(self,K,table_CYK):
        '''metoda zwraca liste pasujacych terminali'''
        tmp = []
        for x in K:
            for a in table_CYK[x[0][0]][x[0][1]]:
                for b in table_CYK[x[1][0]][x[1][1]]:
                    wynik=self.search(str(a)+str(b))
                    print str(wynik)
                    if wynik != -1:
                        for y in wynik:
                            if y != -1:
                                if not y in tmp:
                                    tmp.extend(y)
        if len(tmp)<=0:
            tmp = [-1]
        return tmp
        

G = gramatyka()

K =  G.szukajPar(2,0)
#G = gramatyka()
#print G.getGramarStr()
table_CYK = G.CYK("aabb")


print "final:"
for x in table_CYK:
    print x
L = G.szukajPar(1,2)
M = G.szukajTerminal(L,table_CYK)
print str(M)