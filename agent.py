from map import Map
import constant



class Troops:
    def __init__(self, camp, kind, life, moveRange, attack):
        map = Map()
        self.camp = camp
        self.kind=kind
        self.life=life
        self.moveRange=moveRange
        self.attack=attack
        self.posX,self.posY=map.allocLocation(self)

    def move(self,newX,newY):
        self.posX=newX
        self.posY=newY
        
    def doAttack(self,enemyAgent,enemyTroops):
        enemy.target.life-=self.attack

    def legalAttack(self):
        map=Map()
        x,y=self.posX,self.posY
        legalAttackDic={}
        if self.kind=='general' or self.kind==infantry:
            for i in range(1):
                for j in range(1):
                    if isEnemey(x,y):


                        return legalAttackDic
        if self.kind==cavalry:

            return legalAttackRange

        if self.kind==archer:


            return legalAttackRange


class Agent:
    def __init__(self,index):
        
        if index == 0:
            self.player = constant.player1
        else:
            self.player = constant.player2
                
        self.index=index
        self.general=Troops(self.player['camp'], self.player['general'], 10, 1, 3)
        self.cavalry=Troops(self.player['camp'], self.player['cavalry'], 10, 3, 2)
        self.archer=Troops(self.player['camp'], self.player['archer'], 10, 2, 1)
        self.infantry1=Troops(self.player['camp'], self.player['infantry'], 10, 2, 1)
        self.infantry2=Troops(self.player['camp'], self.player['infantry'], 10, 2, 1)
        
    def isLose(self):
        if self.general.life==0:
            return True
        else:
            return False

    def aliveList(self):
        aliveList=[]
        if self.general.life!=0:
            aliveList.add(self.general)
        if self.cavalry.life!=0:
            aliveList.add(self.cavalry)
        if self.archer.life!=0:
            aliveList.add(self.archer)
        if self.infantry1.life!=0:
            aliveList.add(self.infantry1)
        if self.infantry2.life!=0:
            aliveList.add(self.infantry2)
        return aliveList


"""
    def doRandomActions(self):
        
        for x in aliveList:
    

while player1.isLose()==False and player2.isLose()==False:
    playList=[]
    end=False
    while end==False:
    



p1=Agent(0)

print p1.archer.posX,p1.archer.posY
map=Map()
"""
