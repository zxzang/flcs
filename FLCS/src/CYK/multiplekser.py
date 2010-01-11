##klasa ta reperezentowac bedzie gramatyke
# trzeba zamontowac tutaj funkcje umozliwiajace edycje gramtyki
# narazie bedzie to jedynie statyczna klasa posiadajaca jedna gramtyke na sztywno
class gramatyka():
    def __init__(self):
    #Gramatyka w postaci slownika
        self.G = {"S":["AB","BC"],"A":["BA","a"],"B":["CC","b"],"C":["AB","a"]}

    def add(self, A, B):
        if self.G.has_key(A):    
            self.G[A].append(B)
        else:
            self.G[A] = [B]
        
            
    def search(self,terminal):
        find = 0
        self.result = []
        for x in self.G:
            for T in self.G[x]:
                if T == terminal:
                  find = 1
                  self.result.append(x)  
        if find == 1:    
            return self.result
        else:
            return -1

##klasa bedzie udawac zachowanie multiplekasera, bede jej uzywac do testow
class multiplekser():
    pass

##Implementacja algorytmu CYK
def CYK(G, slowo):
    tmp = []
    table_CYK =[]
    final = []
    #peirwsza czesc odpowiadajaca za wypelnienie pierwszego wiersza w tabeli
    for x in slowo:
        tmp.append(G.search(x))
    table_CYK.append([])
    table_CYK[0] = tmp[0:]
    
    #tutaj jakas totalna masakra taka ze glowa mala:):
    table_CYK.append([])
    poziom=0
    
    k=0
    while k < len(table_CYK[0])-poziom-1:
        #for y in table_CYK[0][1:len(table_CYK[0])]:
        tmp=[]
        x = table_CYK[0][k]
        y = table_CYK[0][k+1]
        #print "pary dla"
        #print x
        #print y
        #print "y"
        #print y
        for a in x:
            for b in y:
                #print "koniunkacja:"
                #print a+b
                wynik = G.search(a+b)
                print wynik
                if wynik != -1:
                    if (wynik in tmp) == False:
                        tmp.extend(wynik)
            #pass
        print "znalezione przypozadkowania:"
        print tmp
        if len(tmp) <= 0:
            tmp = -1
        table_CYK[1].append(tmp)
        k+=1
    #print "tmp"
    #print tmp
    return table_CYK


G = gramatyka()
#print "gramatyka:"
#print G.G
#A = G.search("AB")
#print A
K = CYK(G,"aabbab")
print "final:"
for x in K:
    print "tabela CYK:"
    print x

