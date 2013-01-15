from map import Map
import constant

map = Map()

def distance(node1, node2):
    return abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
    
def maxInjury(troop, node):
    """return degree of injury"""
    player1List, player2List =  map.getSurrounder(node)
    if troop.camp == constant.player1['camp']:
        enemyList = player2List
    if troop.camp == constant.player2['camp']:
        enemyList = player1List

    maxInjuryValue = 0
    for enemy in enemyList:
        maxInjuryValue += enemy['attack']

    if maxInjuryValue == 0:
        injury = 'none'
    elif maxInjuryValue < 3:
        injury = 'low'
    elif maxInjuryValue >= 3 and maxInjuryValue < 5:
        injury = 'medium'
    elif maxInjuryValue >= 5:
        injury = 'heavy'

    return injury

def generalSituation(agent, troop, node):
    player1List, player2List =  map.getSurrounder(agent.generalPosition())
    if agent.camp == constant.player1['camp']:
        numOfTeammates = len(player1List)
        numOfEnemies = len(player2List)
    if agent.camp == constant.player2['camp']:
        numOfTeammates = len(player2List)
        numOfEnemies = len(player1List)

    distanceFromTroop = distance(agent.generalPosition(), troop.currentPosition())
    distanceFromTarget = distance(agent.generalPosition(), node)
    if distanceFromTarget > 2 and distanceFromTroop <= 2:
        numOfTeammates -= 1

    surroundValue = numOfTeammates - numOfEnemies
    generalLife = agent.general.life
    expectedValue = generalLife + surroundValue
    if expectedValue > 10:
        return 'safe'
    elif expectedValue < 5:
        return 'dangerous'
    else:
        return 'normal'

def situation(troop, node):
    """return the expected value of the situation"""
    player1List, player2List =  map.getSurrounder(node)
    if troop.camp == constant.player1['camp']:
        enemyList = player2List
        teammateList = player1List
    if troop.camp == constant.player2['camp']:
        enemyList = player1List
        teammateList = player2List

    ourTotalLife = 0
    ourTotalAttack = 0
    for teammate in teammateList:
        ourTotalLife += teammate['life']
        ourTotalAttack += teammate['attack']

    moveDistance = distance(troop.currentPosition(), node)
    if  moveDistance > 2:
        ourTotalLife += troop.life
        ourTotalAttack += troop.attack

    enemyTotalLife = 0
    enemyTotalAttack = 0
    for enemy in enemyList:
        enemyTotalLife += enemy['life']
        enemyTotalAttack += enemy['attack']

    expectedValue = (ourTotalLife - enemyTotalAttack) - (enemyTotalLife - ourTotalAttack)
    if expectedValue > 0:
        return 'strong'
    elif expectedValue < 0:
        return 'weak'
    elif expectedValue == 0:
        return 'even'

def maxAttackOnGeneral(troop, node):
    x, y = node[0], node[1]
    attackList = map.legalAttacks(troop, x, y)
    for enemy in attackList:
        if enemy['targetTroopId'] == 1:
            return troop.attack

    return 0

def getExpectedValue(agent, troop, node, detail=True):
    weightOfAttackEnemyGeneral = {
        'safe'  :    3,
        'normal':    2,
        'dangerous': 1
    }

    weightOfProtectOurGeneral = {
        'safe' :     1,
        'normal':    2,
        'dangerous': 3
    }

    weightOfInjury = {
        'none': 0,         
        'low': -1,
        'medium': -2,
        'heavy': -3
    }

    weightOfSituation = {
        'strong': 8,
        'weak': -8,
        'even': 0
    }

    generalSituationValue = generalSituation(agent, troop, node)

    situationValue = situation(troop, node)
    attackValue = maxAttackOnGeneral(troop, node)
    injuryValue = maxInjury(troop, node)

    expectedValue = weightOfSituation[situationValue] * weightOfProtectOurGeneral[generalSituationValue] \
            + weightOfAttackEnemyGeneral[generalSituationValue] * attackValue + weightOfInjury[injuryValue] - 5
    print 'expectedValue', expectedValue
    if detail:
        info = {
            'general': generalSituationValue,
            'situation': situationValue, 'injury': injuryValue,
            'attackGeneral': attackValue,
            'expectedValue': expectedValue
        }
        return info
    else:
        return expectedValue
