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
        self.fitness = 0.0
        
        
    def setName(self,name):
        self.right=name
    
    def getRight(self):
        return self.right
    
    
    def addPoints(self, poprawnosc):
        '''dodanie opdpowiednio punktow do odpowiednieo parametru u'''      
        self.u[poprawnosc] =self.u[poprawnosc]+1
        
    def getClassifierStr(self):
        return self.left + "--->" + self.right
    