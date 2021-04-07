import random, sys, pygame
from pygame.locals import *

# Set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set up the windows
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32, 0, 1)
pygame.display.set_caption('Dino')

# Set up colors
black = (0,0,0)
white = (255,255,255)
red = (100,0,0)
green = (0,100,0)
blue = (0,0,100)
orange = (100,50,0)
gray = (150,150,150)

# Game variables
lost = False
score = 0.0
FPS = 60

# Set up time
time = 200
# Set up movement variables
MOVESPEED = 5
INITJUMPFORCE = 200
GRAVITY = 10
# Set up floor
floor = pygame.Rect(0,WINDOWHEIGHT - WINDOWHEIGHT / 3 + 50,WINDOWWIDTH,WINDOWHEIGHT - WINDOWHEIGHT / 3 + 50)


# Set up walls
WALLHEIGHT = 200
def generateNewWall():
    return pygame.Rect(WINDOWWIDTH,WINDOWHEIGHT-WINDOWHEIGHT / 3 - WALLHEIGHT + 50,50,WALLHEIGHT)
walls = []

# Set up fruits
FRUITWIDTH = 25
FRUITHEIGHT = 25
def generateNewFruit():
    return pygame.Rect(random.randint(WINDOWWIDTH / 2, WINDOWWIDTH),random.randint(INITJUMPFORCE, floor.top - FRUITHEIGHT),FRUITWIDTH,FRUITHEIGHT)
fruits = []

# Set up player
PLAYERSIZE = 30
jumpForce = 0
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
falling = False
stopJumping = False
intang = False
slow = False
jumpStep = 1
walls.clear()
player = pygame.Rect(0,floor.top - PLAYERSIZE,PLAYERSIZE,PLAYERSIZE)
intangSurface = pygame.Surface((PLAYERSIZE,PLAYERSIZE))
intangSurface.set_alpha(128)
intangSurface.fill(gray)
# Game start
def gameStart():
    walls.clear()
    fruits.clear()
    player.bottom = floor.top
    player.left = 30
# Invert colors
def invertColor(color):
    invcolor = (abs(color[0] - 255),abs(color[1] - 255),abs(color[2] - 255))
    return invcolor
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
                jumpForce = 0
                moveLeft = False
                moveRight = False
                moveUp = False
                moveDown = False
                falling = False
                stopJumping = False
                intang = False
                slow = False
                jumpStep = 1 
                score = 0
                time = 200
            if event.key == K_SPACE:
                intang = True
            if event.key == K_LSHIFT:
                slow = True
                FPS = 30
                red = invertColor(red)
                green = invertColor(green)
                blue = invertColor(blue)
                orange = invertColor(orange)
                black = invertColor(black)
                white = invertColor(white)
                gray = invertColor(gray)

                
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
            if event.key == K_SPACE:
                intang = False
            if event.key == K_LSHIFT:
                slow = False
                FPS = 60
                red = invertColor(red)
                green = invertColor(green)
                blue = invertColor(blue)
                orange = invertColor(orange)
                black = invertColor(black)
                white = invertColor(white)
                gray = invertColor(gray)
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
    if (
            moveUp 
        and not falling 
        and player.top > WINDOWHEIGHT / 3 
        and not stopJumping
        ):
        jumpForce = INITJUMPFORCE
    if (
            jumpStep != 60 or falling 
        and player.bottom < floor.top
        ):
        jumpForce -= GRAVITY
        player.top -= jumpForce / 30
        jumpStep += 1
    if jumpStep == 60 and not falling:
        jumpStep = 1
    # JUMP AND GRAVITY END

    # PLAYER MOVEMENT END

    # WALL GENERATION
    if len(walls) == 0:
        walls.append(generateNewWall())
    elif(
            len(walls) < 3
        and walls[len(walls)-1].right < WINDOWWIDTH - 150 
        and random.randint(0,60) == 0
        ):
        walls.append(generateNewWall())
    # WALL GENERATION END

    # WALL MOVEMENT
    for wall in walls:
        wall.left -= MOVESPEED / 2
        if(wall.right <= 0):
            walls.remove(wall)
        elif Rect.colliderect(wall, player) and not intang:
            lost = True
    # WALL MOVEMENT END

    # FRUIT GENERATION
    if len(fruits) < 2:
        fruits.append(generateNewFruit())
    for wall in walls:
        for i in range(len(fruits)):
            if (
                    wall.left < fruits[i].left < wall.right
                or  len(fruits) == 2 and fruits[i-1].left < fruits[i].left < fruits[i-1].right
                ):
                fruits.remove(fruits[i])
                fruits.append(generateNewFruit())
    # FRUIT GENERATION END

    # FRUIT MOVEMENT
    for fruit in fruits:
        fruit.left -= MOVESPEED / 2
        if fruit.right <= 0:
            fruits.remove(fruit)
        elif fruit.colliderect(player) and not intang:
            fruits.remove(fruit)
            score += 15
            time += 25
    # FRUIT MOVEMENT END

    # SCORE AND TIME
    score +=0.1
    time -=0.25
    timebar = pygame.Rect(20, 20, time, 20)
    if time <= 0:
        lost = True
    if intang:
        time -=1
    if slow:
        time -=1
    # UPDATE SCREEN
    windowSurface.fill(black)
    if len(walls) != 0:
        for wall in walls:
            pygame.draw.rect(windowSurface,red,wall)
    if len(fruits) != 0:
        for fruit in fruits:
            pygame.draw.rect(windowSurface,orange,fruit)
    if time > 0:
        pygame.draw.rect(windowSurface,blue,timebar)
    pygame.draw.rect(windowSurface,green,floor)
    if not intang:
        pygame.draw.rect(windowSurface,white,player)
    else:
        windowSurface.blit(intangSurface, (player.x, player.y))
    pygame.display.update()
    mainClock.tick(FPS)
    # UPDATE SCREEN END
    
    # LOSE
    basicFont = pygame.font.SysFont(None, 24)
    text = basicFont.render('Final score : %s' % (round(score)), True, black, white)
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
                    if(slow):
                        red = invertColor(red)
                        green = invertColor(green)
                        blue = invertColor(blue)
                        orange = invertColor(orange)
                        black = invertColor(black)
                        white = invertColor(white)
                        gray = invertColor(gray)
                        FPS = 60
                    gameStart()
                    score = 0
                    lost = False
                    jumpForce = 0
                    moveLeft = False
                    moveRight = False
                    moveUp = False
                    moveDown = False
                    falling = False
                    stopJumping = False
                    intang = False
                    slow = False
                    jumpStep = 1       
                    time = 200
                    break
    # END LOSE
