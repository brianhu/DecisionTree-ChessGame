import ConfigParser
from random import randint


class Map(object):
    def __init__(self, filename='level.map'):
        self.map = []
        human_agent_list = ['G','A','C','I','I']
        computer_agent_list = ['g','a','c','i','i']
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.map = parser.get('level', 'map').split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc

        for agent in human_agent_list:
            agent_added = False
            while not agent_added:
                x = randint(0,4)
                y = randint(0,9)
                if self.map[x][y] == '.':
                    buffer = list(self.map[x])
                    buffer[y] = agent
                    buffer = "".join(buffer)
                    self.map[x] = buffer
                    agent_added = True
                

        for agent in computer_agent_list:
            agent_added = False
            while not agent_added:
                x = randint(5,9)
                y = randint(0,9)
                if self.map[x][y] == '.':
                    buffer = list(self.map[x])
                    buffer[y] = agent
                    buffer = "".join(buffer)
                    self.map[x] = buffer
                    agent_added = True


        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_info(self, x, y):
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

    def is_enamy(self, x, y, camp):
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

    def is_teammate(self, x, y, camp):
        """
            this method is used to check whether there is an enamy
            on a specific grid.
        """
        grid_info = self.get_info(x, y)
        try:
            return grid_info['camp'] == camp
        except KeyError:
            return False
