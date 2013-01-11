from map import Map
import constant



class Troops:
    def __init__(self,id, camp, kind, life, moveRange, attack, parent):
        map = Map()
        self.id = id
        self.parent = parent
        self.camp = camp
        self.kind=kind
        self.life=life
        self.moveRange=moveRange
        self.attack=attack
        self.posX,self.posY=map.allocLocation(self)

    def move(self,newX,newY):
        self.posX=newX
        self.posY=newY
        
    def doAttack(self,enemyAgent,enemyTroop):
        enemyTroop.life = enemy.target.life - self.attack

    def currentPosition(self):
        return self.posX, self.posY


class Agent:
    def __init__(self,index):
        
        if index == 0:
            self.player = constant.player1
        else:
            self.player = constant.player2
                
        self.index=index
        self.camp = self.player['camp']
        self.general=Troops(1, self.camp, self.player['general'], 10, 1, 3, index)
        self.cavalry=Troops(2, self.camp, self.player['cavalry'], 10, 3, 2, index)
        self.archer=Troops(3, self.camp, self.player['archer'], 10, 2, 1, index)
        self.infantry1=Troops(4, self.camp, self.player['infantry'], 10, 2, 1, index)
        self.infantry2=Troops(5, self.camp, self.player['infantry'], 10, 2, 1, index)
        
    def isLose(self):
        if self.general.life==0:
            return True
        else:
            return False

    def aliveList(self):
        aliveList=[]
        if self.general.life > 0:
            aliveList.append(self.general)
        if self.cavalry.life > 0:
            aliveList.append(self.cavalry)
        if self.archer.life > 0:
            aliveList.append(self.archer)
        if self.infantry1.life > 0:
            aliveList.append(self.infantry1)
        if self.infantry2.life > 0:
            aliveList.append(self.infantry2)
        return aliveList

    def memberList(self):

        return [self.general,self.cavalry,self.archer,self.infantry1,self.infantry2]

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
