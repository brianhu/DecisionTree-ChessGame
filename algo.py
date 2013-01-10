from agent import Agent
from agent import Troops
from map import Map
from random import randint

def randomMove(agent,map):
    #print agent.memberList()
    #print agent.general.life
    moveList = agent.aliveList()
    attackList = agent.aliveList()
    #print attackList

    while True:
        if len(moveList)==0:
            break
        else:
            num1 = randint(0,len(moveList)-1)
            print num1
            #print 'len:',len(agent.aliveList())
            #print agent.aliveList
        
            troop = moveList[num1]
            
            legalMoves = map.legalActions(troop)
            num2 = randint (0,len(legalMoves)-1)
            chosenMove = legalMoves[num2]
            newX,newY = chosenMove['target']
            troop.posX,troop.posY = newX, newY
            print 'troop ',troop.kind,'from ',chosenMove['start'],'to ',chosenMove['target']
            map.setInfo(troop, (newX,newY))
            moveList.remove(troop)
        

"""

#start,target,targetposition
def legalAttack(self, character):
    attackList = []
    x,y = character.posX ,character.posY
    if character.kind == :
        getInfo(x+1,y)     
"""


"""
def infoDisplayUpdate(agent1,agnet2):
    
    print 'Player1'
    for troop in agent1.memeberList():
            if troop in agent1.aliveList():
            print troop.type,' ',troop.life
    print 'Player2'
    for troop in agent2.memeberList():
        if troop in agent2.aliveList():
            print troop.type,' ',troop.life     
"""
