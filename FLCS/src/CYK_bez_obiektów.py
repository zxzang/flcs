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
        tmp = []
        table_CYK =[]
        final = []
        #peirwsza czesc odpowiadajaca za wypelnienie pierwszego wiersza w tabeli
        for x in slowo:
            a = self.search(x)
            if a == -1:
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
                                  wynik = self.search(str(a)+str(b))
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
                                wynik = self.search(str(b)+str(a))
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
        
        
        
##klasa bedzie udawac zachowanie multiplekasera, bede jej uzywac do testow
class classifier():
    '''klasa bedzie representowac klasyfikator w systemie'''
    def __init__(self,name):
        self.name = name
        
    def set(self,name):
        self.name=name
        
    def getName(slef):
        return slef.name
        

G = gramatyka()
K =  G.CYK("aabb")
#G = gramatyka()
#print G.getGramarStr()
#K = G.CYK("abaaaaabbaba")
print "final:"
for x in K:
    print x
