import pygame, sys
from map import Map
from pygame.locals import *
from agent import Agent
from random import randint
from algo import randomMove

BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption('Hello World!')
fontObj = pygame.font.Font('MONACO.ttf', 32)
map = Map()

player = [Agent(0),Agent(1)]
#player[0] = Agent(0)
#player[1] = Agent(1)

def setMap():
    x_position = 200
    y_position = 40
    for row in map.map:
        textSurfaceObj = fontObj.render(row, True, GREEN, BLUE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x_position, y_position)
        screen.blit(textSurfaceObj, textRectObj)
        y_position += 40

def infoUpdate(agent1,agent2,i):
    print 'Round:',(i+1)/2
    print 'Player1'
    for troop in agent1.memberList():
        if troop in agent1.aliveList():
            print troop.kind,' ',troop.life
    print 'Player2'
    for troop in agent2.memberList():
        if troop in agent2.aliveList():
            print troop.kind,' ',troop.life    

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

i = 1
nowPlayer=player[0]

while True:

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            #print 'nowPlayer:',nowPlayer.index
            if nowPlayer.index == 0:
                randomMove(nowPlayer,map)         
            else:
                randomMove(nowPlayer,map)
            pygame.display.update()
                
            infoUpdate(player[0],player[1],i)
            if player[0].isLose():
                print 'Player2 WIN!!'
                break
            if player[1].isLose():
                print 'Player1 WIN!!'
                break
            nowPlayer = player[ (nowPlayer.index+1)%2 ]
            i = i+1 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    

"""
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
"""



    


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
