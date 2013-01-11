from agent import Agent
from agent import Troops
from map import Map
import random

def randomMove(agentList,agent,map):
    #print agent.memberList()
    #print agent.general.life
    moveList = agent.aliveList()
    #attackList = agent.aliveList()
    #print attackList

    while True:
        if not moveList:
            break
        else:
            #print 'len:',len(agent.aliveList())
            #print agent.aliveList
            
            troop = random.choice(moveList)
            attackList = map.legalAttacks(troop)
            if attackList:
                print 'attackList is not empty'
                print attackList
                map.doAttack(agentList,troop,attackList[0]['targetTroopId'])
                print troop.kind,'attacks',attackList[0]['targetTroopId']
                moveList.remove(troop)
            else:
                actions = map.legalActions(troop)
                action = random.choice(actions)
                print 'troop ',troop.kind,'from ',action['start'],'to ',action['target']
                map.setInfo(troop, action['target'])
                moveList.remove(troop)
        



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
