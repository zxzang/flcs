#-*- coding: utf-8 -*-

class classifier():
    '''klasa bedzie representowac klasyfikator w systemie'''
    def __init__(self,name, left):
        #prawa strona kalsyfikatora
        self.left = left;
        self.right = name
        '''ilosc uzyc jest realizowana za pomoca tablicy 
        u[0] -> ilosc uzyc klasyfikatora przy parsowaniu zdania niepoprawnego
        u[1] -> ilosc uzyc klasyfikatora przy parsowaniu zdania poprawnego'''
        #ilosc poprawnych uzyc
        self.u = []
        self.u.append(0.0)
        #ilosc niepoprawnych uzyc
        self.u.append(0.0)
        
        #co to bylo ??;), czy mam to updejtowac dopiero po rozbiorze?
        self.p = 0.0
        self.d =0.0
        self.r1 = 0.0
        self.r2 = 0.0 
        self.fitness = 0.0
        self.omega = 1.0
        
    def __len__(self):
        return len(self.right)
    
    def __repr__(self):
        return self.left +"-->" + self.right
    
    def compare(self,other):
        ''' metoda porównuje dwa klasyfikaotry jak u GCS'''
        result = 0
        if self.left == other.left:
            result += 1
        for x in range(0,len(self.right)):
            try:
                if self.right[x] == other.right[x]:
                    result += 1
            except:
                pass
        return result
    
    def resetParams(self):
        ''' resetuje paramtery classyfikatora'''
        self.u[0] = 0
        self.u[1] = 0
        #co to bylo ??;), czy mam to updejtowac dopiero po rozbiorze?
        self.p = 0.0
        self.d =0.0
        self.fitness = 0.0
        
    #def __cmp__(self,other):
        #result = 0
        #if self.left == other.left:
            #result += 1
        #for x in range(0,len(self.right)-1):
            #if self.rigt[x] == other.right[x]:
                #result += 1
        #return result
        
    def setName(self,name):
        self.right=name
        
    def setLeft(self,left):
        self.left=left
    
    def getRight(self):
        return self.right

    
    def addPoints(self, poprawnosc):
        '''dodanie opdpowiednio punktow do odpowiednieo parametru u'''      
        self.u[poprawnosc] =self.u[poprawnosc]+1
        
    def getClassifierStrExt(self):
        return self.left + "--->" + self.right +"\t"+"un= "+str(self.u[0])+"\t"+"up="+str(self.u[1])+"\t fitnes"+str(self.fitness)+ "  p i d  "+"("+str(self.p)+","+str(self.d)+")"+ " " + str(self.omega)+'\n'
    #" r1 "+str( self.r1)+" r2 "+str(self.r2)+"\n"
    
    def getClassifierStr(self):
        return self.left + "--->" + self.right