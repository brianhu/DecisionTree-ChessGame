class Troops:
    def __init__(life,MVrange,ATK,ATKrange):
        self.life=life
        self.movement=MVrange
        self.ATK=ATK
        self.ATKrange=ATKrange
        self.posX,self.posY=map.initPosition() 

    def move(self,newX,newY):
        self.posX=newX
        self.posY=newY
        
    def attack(self,enemyAgent,enemyTroops):
        enemy.target.life-=self.ATK
        

        
class Agent:
    def __init__(self,index):
        self.index=index
        self.general=Troops(10,1,3,)
        self.cavalry=Troops(10,3,2,)
        self.archer=Troops(10,2,1,)
        self.infantry1=Troops(10,2,1,)
        self.infantry2=Troops(10,2,1,)
    
        
    def aliveList(self):
        aliveList=[]
        if self.general.life!=0
            aliveList.add(self.general)
        if self.cavalry.life!=0
            aliveList.add(self.cavalry)
        if self.archer.life!=0
            aliveList.add(self.archer)
        if self.infantry1.life!=0
            aliveList.add(self.infantry1)
        if self.infantry2.life!=0
            aliveList.add(self.infantry2)
        return aliveList
    
class play:

    def legalMove:
        
    def lagalAttack:

    

