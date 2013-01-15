import pygame, sys
from map import Map
from pygame.locals import *
from agent import Agent
from random import randint
#from algo import randomMove
#from searchAlgo import myAlgo
#from searchAlgo import evaluationFunction
#from searchAlgo import enemyAround
#from searchAlgo import teammateAround
#from human import humanAlgo
from algorithm import *

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

def infoUpdate(agentList,i):
    print 'Round:',(i+1)/2
    print 'Player1'
    for troop in agentList[0].memberList():
        if troop in agentList[0].aliveList():
            print troop.kind,' ',troop.life
        else:
            print troop.kind,' ','dead'
    print 'Player2'
    for troop in agentList[1].memberList():
        if troop in agentList[1].aliveList():
            print troop.kind,' ',troop.life
        else:
            print troop.kind,' ','dead'

setMap()
end = 0
i = 1
nowPlayer=player[0]

autoRun = False


if sys.argv[1] == '-a':
	autoRun = True


	
while True:

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if nowPlayer.index == 0:
                #humanAlgo(player,nowPlayer,map)         
				algorithm(player,nowPlayer,map,sys.argv[2])
            else:
                #myAlgo(player,nowPlayer,map)
				algorithm(player,nowPlayer,map,sys.argv[3])
            setMap()
                
            infoUpdate(player,i)
            pygame.display.update()

            if autoRun:
                while not player[0].isLose() and not player[1].isLose():
					nowPlayer = player[ (nowPlayer.index+1)%2 ]
					i = i + 1
					if nowPlayer.index == 0:
						#randomMove(player,nowPlayer,map)
						algorithm(player,nowPlayer,map,sys.argv[2])
					else:
						#myAlgo(player,nowPlayer,map)
						algorithm(player,nowPlayer,map,sys.argv[3])
						#randomMove(player,nowPlayer,map)
					setMap()
					infoUpdate(player,i)
					pygame.display.update()
                
            
            if player[0].isLose():
                print 'Player2 WIN!!'
                sys.exit()
                break
            if player[1].isLose():
                print 'Player1 WIN!!'
                sys.exit()
                break
            nowPlayer = player[ (nowPlayer.index+1)%2 ]
            i = i+1
            
        elif event.type == KEYDOWN:
            #print map.getInfo((5,4))
            print 'keydown'
            # actions = map.legalActions(player[1].cavalry)
            # action = randint(0, len(actions) - 1)
            # target = actions[action]['target']
            # map.setInfo(player[1].cavalry, target)
        elif event.type == MOUSEBUTTONDOWN:
            pass
        
    
    

"""
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
