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
            attackList  = map.legalAttacks(troop)
            if attackList:
                #print 'attackList is not empty'
                #print attackList
                troop.doAttack(agentList,attackList[0]['targetTroopId'])
                print troop.kind,'attacks',attackList[0]['targetTroopId']
                moveList.remove(troop)
            else:
                actions, teammateList, enemyList = map.legalActions(troop)
                action = random.choice(actions)
                print 'troop ',troop.kind,'from ',action['start'],'to ',action['target']
                troop.move(action['target'])
                attackList = map.legalAttacks(troop)
                """
                if attackList:
                    troop.doAttack(agentList,attackList[0]['targetTroopId'])
                    print troop.kind,'attacks',attackList[0]['targetTroopId']
                """
                moveList.remove(troop)

    return agentList


