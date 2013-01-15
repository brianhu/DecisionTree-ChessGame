import constant
from ExpectedValue import *
from map import Map
from DecisionTree import DecisionTree

# map = Map()
# class DecisionTree():
#     def __init__(self):

class Decider(object):
    def __init__(self, trainingData='data/training.dat'):
        self.dt = DecisionTree(training_datafile = trainingData, debug1=0, debug2=0)
        self.dt.get_training_data()
        self.rootNode = self.dt.construct_decision_tree_classifier()

    def play(self, agentList, agent, map):
        troops = agent.aliveList()
        for troop in troops:
            bestValue = float('-inf')
            actions, teammateList, enemyList = map.legalActions(troop)
            for action in actions:
                self.makeDecision(agentList, agent, troop, action, map)


    def makeDecision(self, agentList, agent, troop, action, map):
        s1 = 'general=>' + generalSituation(agent, troop, action['target']) # situation 1
        s2 = 'situation=>' + situation(troop, action['target'])
        s3 = 'injury=>' + maxInjury(troop, action['target'])
        s4 = 'attackGeneral=>' + str(maxAttackOnGeneral(troop, action['target']))

        testSample = [s1, s2, s3, s4]
        try:
            classification = self.dt.classify(self.rootNode, testSample)
        except:
            print 'somethign wrong with dt!' , testSample
            classification = {'positive':0, 'negative':1}
            print classification
                    
        if classification['positive'] > classification['negative']:
            troop.move(action['target'])
            attackList  = map.legalAttacks(troop,troop.posX,troop.posY)
            bestValue = float('inf')
            for enemy in attackList:
                if enemy['targetTroopId'] == 1:
                    target = enemy
                    break
                elif enemy['targetLife'] < bestValue:
                    bestValue = enemy['targetLife']
                    target = enemy
            try:
                troop.doAttack(agentList, target['targetTroopId'])
            except UnboundLocalError:
                pass
        


class Trainer(object):
    def __init__(self, source='data/training.dat'):
        super(Trainer, self).__init__()
        self.f = open(source, 'a')
        self.index = 0

    def train(self, agentList, agent, map, round):
        from random import random
        troops = agent.aliveList()
        for troop in troops:
            bestValue = float('-inf')
            actions, teammateList, enemyList = map.legalActions(troop)
            for action in actions:
                info = getExpectedValue(agent, troop, action['target'])
                # if random() < (0.0123 * round): self.write(info)
                self.write(info)
                if bestValue < info['expectedValue']:
                    bestValue = info['expectedValue']
                    bestAction = action

            troop.move(action['target'])
            attackList  = map.legalAttacks(troop,troop.posX,troop.posY)
            bestValue = float('inf')
            for enemy in attackList:
                if enemy['targetTroopId'] == 1:
                    target = enemy
                    break
                elif enemy['targetLife'] < bestValue:
                    bestValue = enemy['targetLife']
                    target = enemy
            try:
                troop.doAttack(agentList, target['targetTroopId'])
            except UnboundLocalError:
                print 'no attack target!', attackList


    def write(self, info):
        samplePrefix = 'sample_'
        space = '       '
        if info['expectedValue'] > 0: result = constant.positive
        else: result = constant.negative
        data = samplePrefix + str(self.index) +  space \
                + result + space \
                + info[constant.general] + space \
                + info[constant.situation] + space \
                + info[constant.injury] + space \
                + str(info[constant.attackGeneral]) + space + "\n"
        print data
        self.f.write(data)
        self.index += 1

    def complete(self):
        self.f.close()

