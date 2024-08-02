import random #for generating random numbers
import sys #to exit the game sys.exiT
import pygame #basic pygame imports
import pygame.locals 
from pygame.locals import *

#Global variables for the game
FPS = 32
WIDTH = 289
HEIGHT = 511
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
GROUND = HEIGHT * 0.8
SPRITES = {}
SOUNDS = {}
BIRD = 'gallery/sprites/bird1.png'
BG = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome image on the screen
    """
    while True:
        playerx = int(WIDTH/5)
        playery = int((HEIGHT - SPRITES['bird'].get_height())/2)
        messagex = int((WIDTH-SPRITES['message'].get_width())/2)
        messagey = int(HEIGHT*0.13)
        basex=0
        while True:
            for event in pygame.event.get():
                #if user clicks on cross button,close the game
                 if event.type == pygame.QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                     pygame.quit()
                     sys.exit()
            #if the user presses space or up key,start the game for them
                 elif event.type==KEYDOWN and (event.type==K_SPACE or event.key==K_UP):
                     return
                 else:
                     SCREEN.blit(SPRITES['background'],(0,0))
                     SCREEN.blit((SPRITES['bird']),(playerx,playery))    
                     SCREEN.blit(SPRITES['message'],(messagex,messagey))    
                     SCREEN.blit(SPRITES['base'],(basex,GROUND))    
                     
                     pygame.display.update()
                     FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx=int(WIDTH/5)
    playery=int(WIDTH/2)
    basex=0

    #creates two pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()

    #my list of upper pipes
    upperPipes = [
        {'x':WIDTH+200, 'y':newPipe1[0]['y']},
        {'x':WIDTH+200+(WIDTH/2), 'y':newPipe2[0]['y']},
    ]

    #my list of lower pipes
    lowerPipes = [
        {'x':WIDTH+200, 'y':newPipe1[1]['y']},
        {'x':WIDTH+200+(WIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX= -4

    playerVelY= -9 #BIRD GIREGI NICHE
    playerMaxVelY= 10 
    playerMinVelY= -8 
    playerAccY= 1 #accelertion

    playerFlapAccv= -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
             if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                 pygame.quit()
                 sys.exit()
             if event.type==KEYDOWN and (event.type==K_SPACE or event.key==K_UP):
                if playery>0:
                    playerVelY=playerFlapAccv
                    playerFlapped=True
                    SOUNDS['flap'].play()

        crashTest= isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return
        
        #check for score
        playerMidPos= playerx + SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}")
                SOUNDS['point'].play()

        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY +=playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUND - playery - playerHeight)
        
        #move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        
        # if the pipe is out of screen, remove it
        if upperPipes[0]['x']< -SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        #lets blit our sprites now
        SCREEN.blit(SPRITES['background'],(0,0))
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(SPRITES['base'],(basex, GROUND))
        SCREEN.blit(SPRITES['player'],(playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += SPRITES['numbers'][digit].get_width()
        Xoffset= (WIDTH - width)/2

        for  digit in myDigits:
            SCREEN.blit(SPRITES['numbers'][digit],(Xoffset,HEIGHT*0.12))
            Xoffset += SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
        if playery >(GROUND - 45) or playery<0:
            SOUNDS['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = SPRITES['pipe'][0].get_height()
            if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) <= SPRITES['pipe'][0].get_width()):
                SOUNDS['hit'].play()
                return True
        
        for pipe in lowerPipes:
            if (playery + SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) <= SPRITES['pipe'][0].get_width():
                SOUNDS['hit'].play()
                return True
        
        return False


def getRandomPipe():
    """
    generate positons of two pipes for blitting on screen
    
    """
    pipeHeight= SPRITES['pipe'][0].get_height()
    offset = HEIGHT/3
    y2 = offset + random.randrange(0, int(HEIGHT - SPRITES['base'].get_height()- 1.2*offset))
    pipeX = WIDTH + 20
    y1 = pipeHeight - y2 + offset 
    pipe = [
        {'x' : pipeX, 'y' : -y1 }, #upperpipe
        {'x' : pipeX, 'y' : y2 } #lower pipe
    ]
    return pipe


if __name__ == "__main__":
    #this will be the main point where the game will start
    pygame.init() #instialise all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Ruchi')
    SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    SPRITES['bird']=(pygame.image.load(BIRD).convert_alpha())
    SPRITES['message'] = (pygame.image.load('gallery/sprites/message1.png').convert_alpha())
    SPRITES['base'] = (pygame.image.load('gallery/sprites/base.png').convert_alpha())
    SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),#ULTA PIPE
        pygame.image.load(PIPE).convert_alpha() #SIDHA PIPE
    )


    #GAME SOUNDS
    SOUNDS['die'] = pygame.mixer.Sound('gallery/sound/die.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('gallery/sound/hit.wav')
    SOUNDS['point'] = pygame.mixer.Sound('gallery/sound/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/sound/swoosh.wav')
    SOUNDS['flap'] = pygame.mixer.Sound('gallery/sound/flap.wav')

    SPRITES['background'] = pygame.image.load(BG).convert_alpha()
    SPRITES['player'] =  pygame.image.load(BIRD).convert_alpha()

    while True:
        welcomeScreen() #shows welcome screen 
        mainGame() #main game function


    

    






