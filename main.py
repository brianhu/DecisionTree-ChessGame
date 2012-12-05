import ConfigParser
import pygame, sys
from pygame.locals import *


class Map(object):
    def load_map(self, filename='level.map'):
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get('level', 'tileset')
        self.map = parser.get('level', 'map').split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc

        self.width = len(self.map[0])
        self.height = len(self.map)
        return self.map

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


BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
fontObj = pygame.font.Font('freesansbold.ttf', 32)
map = Map()
map = map.load_map()
x_position = 200
y_position = 10

for row in map:
    textSurfaceObj = fontObj.render(row, True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x_position, y_position)
    screen.blit(textSurfaceObj, textRectObj)
    y_position += 40
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
