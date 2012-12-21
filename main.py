import pygame, sys
from map import Map
from pygame.locals import *
from agent import Agent

BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption('Hello World!')
fontObj = pygame.font.Font('MONACO.ttf', 32)
map = Map()
player1 = Agent(0)
player2 = Agent(1)
x_position = 200
y_position = 40

for row in map.map:
    textSurfaceObj = fontObj.render(row, True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x_position, y_position)
    screen.blit(textSurfaceObj, textRectObj)
    y_position += 40


actions = map.legalActions(player2.cavalry) 

temp = []
for action in actions:
    print action
    temp.append(action['target'])
print temp

# print '-------------------------'
# actions = map.legalActions(player2.cavalry) 
# temp = []
# for action in actions:
#     # print action['path']
#     # print action['target']
#     temp.append(action['target'])
# print temp
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            print 'quit'
        elif event.type == KEYDOWN:
            print 'keydown'
        elif event.type == MOUSEBUTTONDOWN:
            print 'mousebuttondown'
            if fist.punch(chimp):
                punch_sound.play() #punch
                chimp.punched()
            else:
                whiff_sound.play() #miss
        elif event.type == MOUSEBUTTONUP:
            fist.unpunch()
