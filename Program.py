import random, sys, pygame
from pygame.locals import *

# Set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32, 0, 1)
pygame.display.set_caption('test')

# Set up colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (100,0,0)
GREEN = (0,100,0)
BLUE = (0,0,255)

# Game variables
lost = False
score = 0.0

# Set up movement variables
MOVESPEED = 5
INITJUMPFORCE = 200
GRAVITY = 10

# Set up walls
WALLHEIGHT = 200
def generateNewWall():
    return pygame.Rect(WINDOWWIDTH - 50,WINDOWHEIGHT - WINDOWHEIGHT / 3 - WALLHEIGHT + 50,50,WALLHEIGHT)
walls = []

# Set up floor
floor = pygame.Rect(0,WINDOWHEIGHT - WINDOWHEIGHT / 3 + 50,WINDOWWIDTH,WINDOWHEIGHT - WINDOWHEIGHT / 3 + 50)


jumpForce = 0
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
falling = False
stopJumping = False
jumpStep = 1
walls.clear()
player = pygame.Rect(0,floor.top - 30,30,30)

# Game start
def gameStart():
    jumpForce = 0
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    falling = False
    stopJumping = False
    jumpStep = 1
    walls.clear()
    player.bottom = floor.top
    player.left = 30
    score = 0

gameStart()

# Main game loop
while True:
    # EVENTS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = True
                moveRight = False
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveUp = True
                moveDown = False
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_TAB:
                gameStart()
                score = 0
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
                stopJumping = True
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
    # EVENTS END

    # PLAYER MOVEMENT
    if moveLeft and player.left != 0:
        player.left -= MOVESPEED
    elif moveRight and player.right != WINDOWWIDTH:
        player.left += MOVESPEED
    
    # JUMP AND GRAVITY
    if jumpForce <= 0:
        falling = True
    if player.bottom >= floor.top:
        falling = False
        jumpForce = 0
        stopJumping = False
        player.bottom = floor.top
    if moveUp and not falling and player.top > WINDOWHEIGHT / 3 and not stopJumping:
        jumpForce = INITJUMPFORCE
    if jumpStep != 60 or falling and player.bottom < floor.top:
        jumpForce -= GRAVITY
        player.top -= jumpForce / 30
        jumpStep += 1
    if jumpStep == 60 and not falling:
        jumpStep = 1
    # JUMP AND GRAVITY END

    # PLAYER MOVEMENT END

    # WALL MOVEMENT
    if len(walls) == 0:
        walls.append(generateNewWall())
    elif len(walls) < 3:
        if walls[len(walls)-1].right < WINDOWWIDTH - 150 and random.randint(0,60) == 0:
            walls.append(generateNewWall())
    else:
        pass
    for wall in walls:
        wall.left -= MOVESPEED / 2
        if(wall.right <= 0):
            walls.remove(wall)
        elif Rect.colliderect(wall, player):
            lost = True
    # WALL MOVEMENT END

    score +=0.1

    # UPDATE SCREEN
    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface,WHITE,player)
    if walls.count != 0:
        for wall in walls:
                pygame.draw.rect(windowSurface,RED,wall)
    pygame.draw.rect(windowSurface,GREEN,floor)
    pygame.display.update()
    mainClock.tick(60)
    # UPDATE SCREEN END
    # LOSE
    basicFont = pygame.font.SysFont(None, 24)
    text = basicFont.render('Final score : %s' % (round(score)), True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery
    while lost:
        windowSurface.blit(text, textRect)
        pygame.display.update()
        mainClock.tick(1)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_TAB:
                    gameStart()
                    score = 0
                    lost = False
                    break
    # END LOSE
