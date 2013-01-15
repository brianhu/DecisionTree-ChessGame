from agent import Agent
from agent import Troops
from map import Map
import random
import copy
import math
from ExpectedValue import *
from learningAlgo import Trainer, Decider


def algorithm(agentList,agent,map,index,trainer,round):
    if index == 'r':
        randomAlgo(agentList,agent,map)
        return 
    if index == 's':
        searchAlgo(agentList,agent,map)
        return 
    if index == 'h':
        humanAlgo(agentList,agent,map)
        return 		
    if index == 't':
        trainer.train(agentList, agent, map, round)
    if index == 'd':
        decider = Decider()
        decider.play(agentList,agent,map)
		
def randomAlgo(agentList,agent,map):
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
            attackList  = map.legalAttacks(troop,troop.posX,troop.posY)
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
                attackList = map.legalAttacks(troop,troop.posX,troop.posY)
                """
                if attackList:
                    troop.doAttack(agentList,attackList[0]['targetTroopId'])
                    print troop.kind,'attacks',attackList[0]['targetTroopId']
                """
                moveList.remove(troop)

    return agentList
	


def distanceToGeneral(tX,tY,gX,gY):
	disX = (tX-gX)*(tX-gX)
	disY = (tY-gY)*(tY-gY)
	return math.sqrt(disX+disY)
	
def archerAround(map,troop):
	count = 0
	x,y = troop.posX,troop.posY
	if map.isEnemy(x+2,y,troop.camp):
		count += 2
	if map.isEnemy(x,y+2,troop.camp):
		count += 2
	if map.isEnemy(x,y-2,troop.camp):
		count += 2
	if map.isEnemy(x-2,y,troop.camp):
		count += 2
	return count

def enemyAround(map,troop):
	count = 0
	x,y = troop.posX,troop.posY
	if map.isEnemy(x+1,y,troop.camp):
		count += 1
	if map.isEnemy(x+1,y+1,troop.camp):
		count += 1
	if map.isEnemy(x+1,y-1,troop.camp):
		count += 1
	if map.isEnemy(x,y+1,troop.camp):
		count += 1
	if map.isEnemy(x,y-1,troop.camp):
		count += 1
	if map.isEnemy(x-1,y+1,troop.camp):
		count += 1
	if map.isEnemy(x-1,y,troop.camp):
		count += 1
	if map.isEnemy(x-1,y-1,troop.camp):
		count += 1
	
	return count

def teammateAround(map,troop):
	
	count = 0
	x,y = troop.posX,troop.posY
	if map.isTeammate(x+1,y,troop.camp):
		count += 1
	if map.isTeammate(x+1,y+1,troop.camp):
		count += 1
	if map.isTeammate(x+1,y-1,troop.camp):
		count += 1
	if map.isTeammate(x,y+1,troop.camp):
		count += 1
	if map.isTeammate(x,y-1,troop.camp):
		count += 1
	if map.isTeammate(x-1,y+1,troop.camp):
		count += 1
	if map.isTeammate(x-1,y,troop.camp):
		count += 1
	if map.isTeammate(x-1,y-1,troop.camp):
		count += 1
	
	return count
	
def evaluationFunction(map,agentList,agent,troop,action,attack):

	score = 0
	enemyIndex = (agent.index+1)%2
	x,y = troop.posX,troop.posY
	tmpMap = copy.deepcopy(map)
	tmpMap.setInfo(troop,action['target'])
	if attack != None:
		agentList[enemyIndex].memberList()[ attack['targetTroopId']-1 ].life -= troop.attack
	
	score += agentList[enemyIndex].general.life
	if troop.id == 3:
		score -= (archerAround(tmpMap,troop) + teammateAround(tmpMap,troop))
	else:
		score += (enemyAround(tmpMap,troop) - teammateAround(tmpMap,troop))
	
	if attack != None:
		if attack['targetTroopId'] == 1:
			score -= 400
		if  attack['targetLife'] < 5:
			score -= 100
	if attack != None:
		score -= 20*(7-attack['targetTroopId'])
	
	score -= 5 * distanceToGeneral(x,y,agentList[enemyIndex].general.posX,agentList[enemyIndex].general.posY)
		
	#recover the value
	if attack != None:
		agentList[enemyIndex].memberList()[ attack['targetTroopId']-1 ].life += troop.attack
	troop.posX,troop.posY = x,y
	
	return score
	
def searchAlgo(agentList,agent,map):

	emenyIndex = (agent.index+1)%2
		#map,troop,action,attack,score
	moveList = agent.aliveList()
	
	while True:
		if not moveList:
			break
		else:
			for troop in agent.aliveList() :
				possibleList = []
				if troop in moveList:
					for action in map.legalActions(troop)[0]:
						#print action[0]['target']
						x,y = action['target'][0],action['target'][1]						
						score = evaluationFunction(map,agentList,agent,troop,action,None)
						#print 'score:',score
						possibleList.append({'troop':troop,'target':(x,y),'attackTargetId':None,'score':score})			
						if map.legalAttacks(troop,x,y):
							for attack in map.legalAttacks(troop,x,y):
								#print 'BBM'
								score = evaluationFunction(map,agentList,agent,troop,action,attack)
								possibleList.append({'troop':troop,'target':(x,y),'attackTargetId':attack['targetTroopId'],'score':score})
				
					sortedList = sorted(possibleList,key = lambda x:x['score'])
					print 'troop:',troop.kind
					i = 0
					#while i < len(sortedList) :
					#	print sortedList[i]['score']
					#	i += 1
					
					sortedList[0]['troop'].move(sortedList[0]['target'])
					print 'troop',troop.kind,'move to ', sortedList[0]['target']
					if sortedList[0]['attackTargetId'] != None:
						troop.doAttack(agentList,sortedList[0]['attackTargetId'])
					print 'troop',troop.kind,'attacks',sortedList[0]['attackTargetId']
	
					moveList.remove(troop)

	return agentList
	
	
def humanAlgo(agentList,agent,map):

	emenyIndex = (agent.index+1)%2
		#map,troop,action,attack,score
	moveList = agent.aliveList()
	
	while True:
		if not moveList:
			break
		else:
			for troop in moveList :
				print troop.id
			i = int(input('Choose a troop:'))
			if i == -1:
				break			
			nowTroop = agent.memberList()[i-1]
			
			count = 0
			for action in map.legalActions(nowTroop)[0]:
				print count,':',action['target']
				count += 1
				
			j = input('Choose a move:')
			nowTroop.move(map.legalActions(nowTroop)[0][j]['target'])
			
			count = 0
			for attack in map.legalAttacks(nowTroop,nowTroop.posX,nowTroop.posY):
				print count,':',attack['targetLocation']
				count += 1
			
			k = input('Choose an target:')
			if k != -1:
				nowTroop.doAttack(agentList,map.legalAttacks(nowTroop,nowTroop.posX,nowTroop.posY)[k]['targetTroopId'])
			
			#setMap()
			moveList.remove(nowTroop)

	return agentList
