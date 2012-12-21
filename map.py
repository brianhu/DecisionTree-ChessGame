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
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.map = parser.get('level', 'map').split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def allocLocation(self, character):
        # player1CharacterList = ['G','A','C','I','I']
        # player2CharacterList = ['g','a','c','i','i']
        agentAdded = False
        while not agentAdded:
            if character.camp == constant.player1['camp']:
                x = randint(0, 4)
            else:
                x = randint(5, 9)
            y = randint(0, 9)
            if character.kind == 'c':
                x, y = (5, 4)
                buffer = list(self.map[x])
                buffer[y] = character.kind
                buffer = "".join(buffer)
                self.map[x] = buffer
                agentAdded = True
            elif character.kind =='C':
                x, y = (4, 4)
                buffer = list(self.map[x])
                buffer[y] = character.kind
                buffer = "".join(buffer)
                self.map[x] = buffer
                agentAdded = True
            elif character.kind == 'I':
                x, y = (4, 3)
                buffer = list(self.map[x])
                buffer[y] = character.kind
                buffer = "".join(buffer)
                self.map[x] = buffer
                agentAdded = True
            elif self.map[x][y] == '.':
                buffer = list(self.map[x])
                buffer[y] = character.kind
                buffer = "".join(buffer)
                self.map[x] = buffer
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
        x = node[0]
        y = node[1]
        try:
            char = self.map[x][y]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def legalActions(self, character):
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


        def addOptions(options=[], invalidPaths=[], fringe=[]):
            if not options:
                option = {
                    'start': (character.posX, character.posY),
                    'path': [],
                    'cost': 0,
                    'target': (character.posX, character.posY)
                } # stop is always an option
                options.append(option)
                fringe.append(option)

            newFringe = []
            for option in fringe:
                if option['cost'] < character.moveRange:
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
                                        'target': node
                                    }
                                    newFringe.append(newOption)
                                elif info['camp'] != character.camp:
                                    for border in getBorder(node):
                                        invalidPaths.append(border)
                            except KeyError:
                                # if x, y are out of range, KeyError may be triggered
                                pass
                else:
                    print '-----------options-------'
                    print options
                    print '========================='
                    for o in options:
                        print '$$$$$$$$$$$$'
                        print o['target']
                        print '$$$$$$$$$$$$'
                        if o['target'] == (5, 2):
                            print 'fffffffffffffff'
                        for path in invalidPaths:
                            if path in o['path'][:-1]:
                                print 'invalid'
                                print path
                                print o
                                options.remove(o)
                                terminated = True
                                break
                    return options
            for option in newFringe:
                options.append(option)
            options = addOptions(options, invalidPaths, newFringe)
            return options

        actions = addOptions()
        return actions

    def isEnemy(self, character):
        """
            this method is used to check whether there is an enamy
            on a specific grid.
        """
        enemyMap = {
            'player1' : 'player2',
            'player2' : 'player1'
        }
        node = (character.posX, character.posY)
        gridInfo = self.getInfo(node)
        try:
            return grid_info['camp'] == enemyMap[camp]
        except KeyError:
            return False

    def isTeammate(self, x, y, camp):
        """
            this method is used to check whether there is an enamy
            on a specific grid.
        """
        grid_info = self.get_info(x, y)
        try:
            return grid_info['camp'] == camp
        except KeyError:
            return False
