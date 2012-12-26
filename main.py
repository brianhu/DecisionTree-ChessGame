import pygame, sys
from map import Map
from pygame.locals import *
from agent import Agent
from random import randint

BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption('Hello World!')
fontObj = pygame.font.Font('MONACO.ttf', 32)
map = Map()
player1 = Agent(0)
player2 = Agent(1)

def setMap():
    x_position = 200
    y_position = 40
    for row in map.map:
        textSurfaceObj = fontObj.render(row, True, GREEN, BLUE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x_position, y_position)
        screen.blit(textSurfaceObj, textRectObj)
        y_position += 40


# actions = map.legalActions(player1.cavalry) 
# 
# temp = []
# for action in actions:
#     print action
#     temp.append(action['target'])
# print temp

# print '-------------------------'
# actions = map.legalActions(player2.cavalry) 
# temp = []
# for action in actions:
#     # print action['path']
#     # print action['target']
#     temp.append(action['target'])
# print temp
setMap()
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
            actions = map.legalActions(player2.cavalry)
            action = randint(0, len(actions) - 1)
            target = actions[action]['target']
            map.setInfo(player2.cavalry, target)
            setMap()
        elif event.type == MOUSEBUTTONDOWN:
            print 'mousebuttondown'
            if fist.punch(chimp):
                punch_sound.play() #punch
                chimp.punched()
            else:
                whiff_sound.play() #miss
        elif event.type == MOUSEBUTTONUP:
            fist.unpunch()



# p0=Agent(0)
# p1=Agent(1)
# nowPlayer=p0
# 
# while p0.isLose()==False and p1.isLose()==False:
#     doneList=nowPlayer.aliveList()
#     while len(doneList)!=0:
#         x=algorithm()
#         information update
#         doneList.remove(x)
# 
#     if nowPlayer==p0:
#         nowPlayer=p1
#     else:
#         nowPlayer=p0
