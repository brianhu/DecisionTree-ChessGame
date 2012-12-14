import ConfigParser
from random import randint
from constant import *

class Map(object):
    def __init__(self, filename='level.map'):
        self.map = []
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
        agent_added = False
        while not agent_added:
            if character.isupper():
                x = randint(0,4)
            else:
                x = randint(5,9)
            y = randint(0,9)
            if self.map[x][y] == '.':
                buffer = list(self.map[x])
                buffer[y] = character
                buffer = "".join(buffer)
                self.map[x] = buffer
                agent_added = True

        return x, y

    def getInfo(self, x, y):
        """
            this method is used to get info of a specific grid on map
            a map like:
            ...
            .#.
            ##.
            it's a list: ['...','.#.','##.'] in python
            map[0][1] is .
            map[1][1] is #
        """
        try:
            char = self.map[x][y]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    # def get_available_location(self, x, y, camp, step):
    #     if x + step > self.width:
    #         right_border = self.width
    #     else:
    #         right_border = x + step
    #     if x - step < 0 :
    #         left_border = 0
    #     else:
    #         left_border = x - step
    #     if y + step > self.height:
    #         bottom_border = self.height
    #     else:
    #         bottom_border = y + step
    #     if y - step < 0:
    #         top_border = 0
    #     else:
    #         top_border = y - step

    #     for temp_x in range(left_border, right_border + 1):
    #         if temp_x != x:


    def isEnamy(self, x, y, camp):
        """
            this method is used to check whether there is an enamy
            on a specific grid.
        """
        enamy_map = {
            'human' : 'computer',
            'computer' : 'human'
        }
        grid_info = self.get_info(x, y)
        try:
            return grid_info['camp'] == enamy_map[camp]
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
