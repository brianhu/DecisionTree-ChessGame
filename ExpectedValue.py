from map import Map

map = Map()

def distance(node1, node2):
    return abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
    
def injury(troop, node):
    """return degree of injury"""
    player1List, player2List =  map.getSurrounder(node)
    if troop.camp == constant.player1['camp']:
        enemyList = player2List
    if troop.camp == constant.player2['camp']:
        enemyList = player1List

    maxInjury = 0
    for enemy in enemyList:
        maxInjury += enemy['attack']

    if maxInjury == 0:
        injury = 'none'
    elif maxInjury < 3:
        injury = 'low'
    elif maxInjury >= 3 and maxInjury < 5:
        injury = 'medium'
    elif maxInjury <= 5:
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
    if distanceFromTarget > 2 and distanceFromTarget <= 2:
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

    ourTotalLive = 0
    ourTotalAttack = 0
    for teammate in teammateList:
        ourTotalLive += teammate['live']
        ourTotalAttack += teammate['attack']

    moveDistance = distance(troop.currentPosition(), node)
    if moveDistance > 2:
        ourTotalLive -= troop.life
        ourTotalAttack -= troop.attack

    enemyTotalLive = 0
    enemyTotalAttack = 0
    for enemy in enemyList:
        enemyTotalLive += enemy['live']
        enemyTotalAttack += enemy['attack']

    expectedValue = (ourTotalAttack - enemyTotalLive) + (enemyTotalAttack - ourTotalLive)
    if expectedValue > 0:
        return 'strong'
    elif expectedValue < 0:
        return 'weak'
    elif expectedValue == 0:
        return 'even'

def maxAttackOnGeneral(troop):

