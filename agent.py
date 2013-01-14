from map import Map
import constant


map = Map()

class Agent(object):
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
        self.infantry1=Troops(4, self.camp, self.player['infantry1'], 10, 2, 1, index)
        self.infantry2=Troops(5, self.camp, self.player['infantry1'], 10, 2, 1, index)

        self.distribution = {}
        self.distribution[self.general.currentPosition()] = self.general
        self.distribution[self.cavalry.currentPosition()] = self.cavalry
        self.distribution[self.archer.currentPosition()] = self.archer
        self.distribution[self.infantry1.currentPosition()] = self.infantry1
        self.distribution[self.infantry2.currentPosition()] = self.infantry2
        
    def isLose(self):
        if self.general.life < 0:
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

    def generalPosition(self):
        """return general position"""
        return self.general.currentPosition()
        

class Troops(object):
    def __init__(self,id, camp, kind, life, moveRange, attack, parent):
        self.id = id
        self.parent = parent
        self.camp = camp
        self.kind=kind
        self.life=life
        self.moveRange=moveRange
        self.attack=attack
        self.posX,self.posY=map.allocLocation(self)

    def getDetail(self):
        detail = {
            'id': self.id,
            'camp': self.camp,
            'name': self.kind,
            'life': self.life,
            'attack': self.attack
        }
        return detail

    def move(self, target):
        map.setInfo(self, target)
        originalNode = self.posX, self.posY
        self.posX = target[0]
        self.posY = target[1]
        
    def doAttack(self,agentList,attackedId):
        enemyIndex = (self.parent + 1 ) % 2
        
        if attackedId == 1:
            target = agentList[enemyIndex].general
        if attackedId == 2:
            target = agentList[enemyIndex].cavalry
        if attackedId == 3:
            target = agentList[enemyIndex].archer
        if attackedId == 4:
            target = agentList[enemyIndex].infantry1
        if attackedId == 5:
            target = agentList[enemyIndex].infantry2
        target.life -= self.attack
        if target.life < 0:
            print target.kind, ' dead!'
            map.removeDead(target.currentPosition())

        return agentList

    def currentPosition(self):
        return (self.posX, self.posY)


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
