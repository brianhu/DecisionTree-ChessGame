from map import Map
import pygame, sys
from pygame.locals import *

BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption('Hello World!')
fontObj = pygame.font.Font('MONACO.ttf', 32)
map = Map()
x_position = 200
y_position = 40

for row in map.map:
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
