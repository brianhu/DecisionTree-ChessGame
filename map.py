import ConfigParser 
from random import randint
import constant
import copy

def singleton(cls):
    sharedMap = {}
    def getSharedMap():
        if cls not in sharedMap:
            sharedMap[cls] = cls()
        return sharedMap[cls]
    return getSharedMap

@singleton
class Map(object):
    def __init__(self, filename='level.map'):
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.map = parser.get('level', 'map').split("\n")
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.distribution = {}

    def update(self, node, value):
        x = node[0]
        y = node[1]
        buffer = list(self.map[x])
        buffer[y] = value
        buffer = "".join(buffer)
        self.map[x] = buffer
    def setDistribution(self, originalNode, target):
        self.distribution[target] = self.distribution.pop(originalNode)

    def allocLocation(self, troop):
        # player1CharacterList = ['G','A','C','I','I']
        # player2CharacterList = ['g','a','c','i','i']
        agentAdded = False
        while not agentAdded:
            if troop.camp == constant.player1['camp']:
                x = randint(0, 4)
            else:
                x = randint(5, 9)
            y = randint(0, 9)
            if self.map[x][y] == '.':
                self.update((x, y), troop.kind)
                self.distribution[(x, y)] = troop
                agentAdded = True

        return x, y

    def getInfo(self, node):
        """
            this method is used to get info of a specific grid on map
            a map like:
            .#.
            ...
            ...
            it's a list: ['...','.#.','##.'] in python
            map[0][0] is .
            map[0][1] is #
        """
        if node[0] < 0 or node[1] < 0 or node[0] > 9 or node[1] > 9: # out of map range
            return None
        try:
            return self.distribution[node].getDetail()
        except KeyError:
            return {'camp': 'neutral', 'name': 'floor'}

    def getSurrounder(self, node):
        """
              *
             ***
            **x**
             ***
              *
            search through all stars
            return surrounding enemis and teammates
        """
        x = node[0]
        y = node[1]
        player1List = []
        player2List = []
        surrounder = []
        for tempX in range(x-1, x+2):
            for tempY in range(y-1, y+2):
                tempNode = (tempX, tempY)
                if tempNode != node:
                    surrounder.append(tempNode)
        surrounder.append((x-2, y))
        surrounder.append((x+2, y))
        surrounder.append((x, y+2))
        surrounder.append((x, y-2))

        for node in surrounder:
            info = self.getInfo(node)
            try:
                if info['camp'] == constant.player1['camp']:
                    player1List.append(info)
                elif info['camp'] == constant.player2['camp']:
                    player2List.append(info)
            except (KeyError, TypeError):
                pass
        return player1List, player2List


    def setInfo(self, troop, target):
        """update map"""
        self.update((troop.posX, troop.posY), '.')

        self.update(target, troop.kind)
        self.setDistribution((troop.posX, troop.posY), target)

    def legalActions(self, troop):
        """return legal locatoins"""
        import copy
        def getBorder(node):
            x = node[0]
            y = node[1]
            border = []
            if x != 0:
                border.append(((x-1), y))
            if x != 9:
                border.append(((x+1), y))
            if y != 0:
                border.append((x, (y-1)))
            if y != 9:
                border.append((x, (y+1)))
            return border

        def addOptions(options=[], teammateList=[], enemyList=[], invalidPaths=[], fringe=[]):
            if not options:
                option = {
                    'start': (troop.posX, troop.posY),
                    'path': [],
                    'cost': 0,
                    'stop': True,
                    'target': (troop.posX, troop.posY)
                } # stop is always an option
                options.append(option)
                fringe.append(option)

            newFringe = []
            for option in fringe:
                if option['cost'] < troop.moveRange:
                    start = option['target'] # start of next step is target of last step
                    checkList = getBorder(start)
                    for node in checkList:
                        path = copy.copy(option['path'])
                        if node not in path:
                            info = self.getInfo(node)
                            try:
                                if info['name'] == 'floor':
                                    path.append(node)
                                    newOption = {
                                        'start': option['start'],
                                        'path': path,
                                        'cost': option['cost'] + 1,
                                        'stop': True,
                                        'target': node
                                    }
                                    newFringe.append(newOption)
                                elif info['camp'] != troop.camp:
                                    enemyList.append(info)
                                    for border in getBorder(node):
                                        invalidPaths.append(border)
                                elif info['camp'] == troop.camp:
                                    teammateList.append(info)
                                    path.append(node)
                                    newOption = {
                                        'start': option['start'],
                                        'path': path,
                                        'cost': option['cost'] + 1,
                                        'stop': False,
                                        'target': node
                                    }
                                    newFringe.append(newOption)
                            except KeyError:
                                # if x, y are out of range, KeyError may be triggered
                                pass
                else:
                    invalidOptions = []
                    for option in options:
                        for path in invalidPaths:
                            if path in option['path'][:-1]:
                                invalidOptions.append(option)
                                break
                    for option in invalidOptions:
                        options.remove(option)
                    return options, teammateList, enemyList
            for option in newFringe:
                if option['stop']:
                    options.append(option)
            options, teammateList, enemyList = addOptions(options, teammateList, enemyList, invalidPaths, newFringe)
            return options, teammateList, enemyList

        actions, teammateList, enemyList = addOptions()
        return actions, teammateList, enemyList

    def isEnemy(self, x, y, camp):
        """
            this method is used to check whether there is an enemy
            on a specific grid.
            if there is an enemy on a grid, retun the id of it.
            otherwise, return false
        """
        node = (x, y)
        gridInfo = self.getInfo(node)
        try:
            if gridInfo['camp'] == constant.enemyMap[camp]:
                return int(gridInfo['id'])
            else:
                return False
        except (KeyError, TypeError):
            return False

    def isTeammate(self, x, y, camp):
        """
            this method is used to check whether there is an enamy
            on a specific grid.
        """
        grid_info = self.getInfo((x, y))
        try:
            return grid_info['camp'] == camp
        except (KeyError, TypeError):
            return False

    def legalAttacks(self,character,x,y):

        #x,y = character.posX ,character.posY
        attackList = []

        if character.id == 1 or character.id == 4 or character.id == 5:
            if self.isEnemy(x+1,y,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x+1,y,character.camp), 'targetLocation':(x+1,y), 'targetLife':character.life})
            if self.isEnemy(x+1,y+1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x+1,y+1,character.camp), 'targetLocation':(x+1,y+1), 'targetLife':character.life})            
            if self.isEnemy(x+1,y-1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x+1,y-1,character.camp), 'targetLocation':(x+1,y-1), 'targetLife':character.life})
            if self.isEnemy(x,y+1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x,y+1,character.camp), 'targetLocation':(x,y+1), 'targetLife':character.life})
            if self.isEnemy(x-1,y+1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x-1,y+1,character.camp), 'targetLocation':(x-1,y+1), 'targetLife':character.life})
            if self.isEnemy(x-1,y-1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x-1,y-1,character.camp), 'targetLocation':(x-1,y-1), 'targetLife':character.life})
            if self.isEnemy(x,y-1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x,y-1,character.camp), 'targetLocation':(x,y-1), 'targetLife':character.life})
            if self.isEnemy(x-1,y,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x-1,y,character.camp), 'targetLocation':(x-1,y), 'targetLife':character.life})

        if character.id == 2:
            if self.isEnemy(x+1,y,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x+1,y,character.camp), 'targetLocation':(x+1,y), 'targetLife':character.life})
            if self.isEnemy(x-1,y,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x-1,y,character.camp), 'targetLocation':(x-1,y), 'targetLife':character.life})            
            if self.isEnemy(x,y-1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x,y-1,character.camp), 'targetLocation':(x,y-1), 'targetLife':character.life})
            if self.isEnemy(x,y+1,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x,y+1,character.camp), 'targetLocation':(x,y+1), 'targetLife':character.life})

        if character.id == 3:
            if self.isEnemy(x+2,y,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x+2,y,character.camp), 'targetLocation':(x+2,y), 'targetLife':character.life})
            if self.isEnemy(x-2,y,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x-2,y,character.camp), 'targetLocation':(x-2,y), 'targetLife':character.life})            
            if self.isEnemy(x,y-2,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x,y-2,character.camp), 'targetLocation':(x,y-2), 'targetLife':character.life})
            if self.isEnemy(x,y+2,character.camp):
                attackList.append({'start':(x,y), 'targetTroopId':self.isEnemy(x,y+2,character.camp), 'targetLocation':(x,y+2), 'targetLife':character.life})            
              
        return attackList

    def removeDead(self, node):
        """this method is used to remove dead from the map"""
        self.update(node, '.')
        try:
            del self.distribution[node]
        except KeyError:
            print 'error!!!!!!!', self.distribution
