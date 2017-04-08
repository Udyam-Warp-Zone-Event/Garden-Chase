import os
import pygame
import sys
import random
import math
from pygame import *

pygame.init()

scr_size = (width,height) = (900,600)
FPS = 60
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
background_col = (240,240,220)
background_col1 = (153,217,234)

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('sprites',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect

def displaytext(
    text,
    fontsize,
    x,
    y,
    color,
    ):

    font = pygame.font.SysFont('sawasdee', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)


"""def getHighScore():

    highscore = 0
    try:
        highscoreFile = open("highscore.txt","r")
        highscore = int(highscoreFile.read())
        highscoreFile.close()

    #except IOError:

    #except ValueError:
        return highscore

def saveHighScore(newHighScore):
    try:
        highscoreFile = open("highscore.txt","w")
        highscoreFile.write(str(newHighScore))
        highscoreFile.close()

    #except IOError:"""




class Man():
    def __init__(self,sizex=-1,sizey=-1):
        self.images,self.rect = load_sprite_sheet('runningman1.png',5,1,sizex,sizey,-1)
        self.images1,self.rect1 = load_sprite_sheet('car2.png',2,1,80,30,-1)
        self.rect.bottom = height - 100
        self.rect.left = width/10
        self.rect1.right = width/10+44
        self.rect1.bottom = height - 100
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.movement = [0,0]
        self.jumpSpeed = 12
        self.score = 0
        self.movingleft=False
        self.movingright=False
        self.health=100
        self.missile = 20
        self.bullets = 20


        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image,self.rect)

    def checkbounds(self):
        if self.rect.bottom > height - 100:
            self.rect.bottom = height - 100
            self.isJumping = False

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > width:
            self.rect.right = width

        if self.health > 100:
            self.health = 100

        if self.health < 0:
            self.health = 0

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        if self.movingleft:
           self.rect.left -= 3

        if self.movingright:
           self.rect.left += 3

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        self.counter = (self.counter + 1)%1000000000

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('cacti-small.png',6,1,sizex,sizey,-1)
        self.rect.bottom = height - 100
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,5)]
        self.movement = [-5,0]#15,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class MissilePack(pygame.sprite.Sprite):
    def __init__(self,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('missilePack.png',25,40,-1)
        self.rect.bottom = height - 200
        self.rect.left = width + self.rect.width
        #self.image = self.images[random.randrange(0,15)]
        self.movement = [-5,0]#15,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class BulletPack(pygame.sprite.Sprite):
    def __init__(self,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('bulletPack.png',40,25,-1)
        self.rect.bottom = height - 200
        self.rect.left = width + self.rect.width
        #self.image = self.images[random.randrange(0,15)]
        self.movement = [-5,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class HealthPack(pygame.sprite.Sprite):
    def __init__(self,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('healthPack.png',25,25,-1)
        self.rect.bottom = height - 230
        self.rect.left = width + self.rect.width
        #self.image = self.images[random.randrange(0,15)]
        self.movement = [-5,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()



class UFO(pygame.sprite.Sprite):
    def __init__(self,sizex=-1,sizey=-1):
       pygame.sprite.Sprite.__init__(self,self.containers)
       self.images,self.rect = load_sprite_sheet('ufo1.png',3,2,sizex,sizey,-1)
       self.rect.bottom = height/2-90
       self.rect.left = width + self.rect.width
       self.image = self.images[random.randrange(0,5)]
       self.movement = [-7,0]#15,0]
       self.counter = 0
       self.counter1 = -1


       def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,enemy,dist,z):
        self.rect = self.rect.move(self.movement)
        if self.counter%125 == 0:
            self.movement = [-5,0]
        if self.counter%125 == 25:
            self.movement = [-2,-2]
        if self.counter%125 == 50:
            self.movement = [-2,2]
        if self.counter%125 == 75:
            self.movement = [2,2]
        if self.counter%125 == 100:
            self.movement = [2,-2]


        if self.rect.right < 0:
            self.kill()

        if self.rect.centerx - enemy.rect.centerx < dist and self.rect.centerx - enemy.rect.centerx > -dist:
            self.counter1 += 1
            if self.counter%z == 0:
                Bomb(self.rect.centerx,self.rect.bottom,8,20)

        self.counter += 1

class Explode(pygame.sprite.Sprite):
    def __init__(self,posx,posy,sizex=-1,sizey=-1):
       pygame.sprite.Sprite.__init__(self,self.containers)
       self.images,self.rect = load_sprite_sheet('explosion.bmp',5,2,sizex,sizey,-1)                                    #explosion ///////////////////
       self.rect.centerx = posx
       self.rect.centery = posy
       self.image = self.images[0]
       self.movement = [-7,0]#15,0]
       self.counter = 0
       self.counter1 = -1
       self.index = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):

        self.image = self.images[self.index]

        if self.index >= 9:
            self.kill()

        if self.counter%5== 0:
            self.index += 1

        self.counter+=1




class Bomb(pygame.sprite.Sprite):
    def __init__(self,posx,posy,sizex=-1,sizey=-1):                                                 #bullet problem
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('missile.png',sizex,sizey,-1)
        self.rect.top=posy-20
        self.rect.left=posx
        self.movement = [0,2]
        self.kill1 = False

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.top > height-120:
            self.kill()
        if self.kill1:
            self.kill()


class Missile(pygame.sprite.Sprite):
    def __init__(self,posx,posy,sizex=-1,sizey=-1):                                                 #bullet problem
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('missileFire.png',sizex,sizey,-1)
        self.rect.left=posy
        self.rect.bottom=posx
        self.movement = [0,-4]
        self.kill1 = False

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.top < 0:
            self.kill()
        if self.kill1:
            self.kill()


class Bullets(pygame.sprite.Sprite):
    def __init__(self,posx,posy,sizex=-1,sizey=-1):                                                 #bullet problem
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('bullet3.png',sizex,sizey,-1)
        self.rect.top=posy
        self.rect.left=posx
        self.movement = [8,0]
        self.kill1 = False

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.left > width:
            self.kill()
        if self.kill1:
            self.kill()

class Ground():
    def __init__(self,image):
        if image==1:
            self.image,self.rect = load_image('ground6.png',-1,-1,-1)
            self.image1,self.rect1 = load_image('ground6.png',-1,-1,-1)
        if image ==2:
            self.image,self.rect = load_image('ground7.png',-1,-1,-1)
            self.image1,self.rect1 = load_image('ground7.png',-1,-1,-1)

        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = -5

    def draw(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self,man):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right
            man.score += 100                                                   #score adddition problem???????????????????????????/

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
            man.score +=100

class ExitScreen():
    def __init__(self):
        self.image,self.rect = load_image('gameOver.png',width,height,-1)
        self.rect.top = 0
        self.rect.left = 0

    def draw(self):
        screen.blit(self.image,self.rect)

class StartScreen():
    def __init__(self):
        self.image,self.rect = load_image('FINALINTIAL.png',width,height,-1)
        self.rect.top = 0
        self.rect.left = 0

    def draw(self):
        screen.blit(self.image,self.rect)

class LevelScreen():
    def __init__(self):
        self.image,self.rect = load_image('levelscreen.png',width,height,-1)
        self.rect.top = 0
        self.rect.left = 0

    def draw(self):
        screen.blit(self.image,self.rect)

class HelpScreen():
    def __init__(self):
        self.image,self.rect = load_image('instructions.png',width,height,-1)
        self.rect.top = 0
        self.rect.left = 0

    def draw(self):
        screen.blit(self.image,self.rect)


class MissileBar():
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('missileFire.png',30,45,-1)
        self.rect.bottom =80
        self.rect.left = 10

    def draw(self):
        screen.blit(self.image,self.rect)

class BulletBar():
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('bullet3.png',45,20,-1)
        self.rect.bottom = 70
        self.rect.right = width - 100

    def draw(self):
        screen.blit(self.image,self.rect)

class HealthBar():
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('healthPack.png',30,30,-1)
        self.rect.top = 5
        self.rect.left = 10

    def draw(self):
        screen.blit(self.image,self.rect)


def main():
    gameOver = False
    finalGameOver = False
    gameExit = False
    startScreen = False
    levelscreenv =  True
    helpscreenv = False

    #gunshotM = pygame.mixer.Sound('gunshot.wav')                                      #music obj???????????????
    #HIghScore =  getHighScore()

    level1 = False
    level2 = False
    level3 = False

    exitscreen = ExitScreen()
    startscreen = StartScreen()
    levelscreen = LevelScreen()
    helpscreen = HelpScreen()

    playerMan = Man(44,60)



    missilebar = MissileBar()
    bulletbar =  BulletBar()
    healthbar = HealthBar()

    counter = 0                          # counters
    obstacleCounter = 0
    ufocounter = 0
    count = 7
    countU = 250
    counterBM = 1

    bullet = pygame.sprite.Group()
    Bullets.containers = bullet

    bombs = pygame.sprite.Group()
    Bomb.containers = bombs

    explode = pygame.sprite.Group()
    Explode.containers = explode

    missiles = pygame.sprite.Group()
    Missile.containers = missiles

    obstacle = pygame.sprite.Group()
    Obstacles.containers = obstacle
    Obstacles(35,80)

    missilepack = pygame.sprite.Group()
    MissilePack.containers = missilepack

    bulletpack = pygame.sprite.Group()
    BulletPack.containers = bulletpack

    healthpack = pygame.sprite.Group()
    HealthPack.containers = healthpack


    UFOs = pygame.sprite.Group()                                                            # drawing UFO

    UFO.containers = UFOs


    while not finalGameOver:

             gameExit = False

             while not startScreen:


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        startscreen = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            startScreen = True

                        if event.key == pygame.K_h:
                            helpscreenv = True
                            startScreen = True
                        """if event.type == pygame.K_q:
                            gameOver = True
                            gameExit = True
                            finalGameOver = True
                            startScreen = True"""


                screen.fill(background_col1)
                startscreen.draw()

                pygame.display.update()

                clock.tick(FPS)


             while helpscreenv:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        startscreen = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            levelscreenv = True
                            helpscreenv = False

                screen.fill(background_col1)
                helpscreen.draw()
                displaytext("ENTER TO CONTINUE",50,width/2,height/2+80,(20,0,50))
                pygame.display.update()

                clock.tick(FPS)

             while  levelscreenv:
                 for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finalgameover = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
                            level1 = True
                            levelscreenv = False

                        if event.key == pygame.K_i:
                            level2 = True
                            levelscreenv = False

                        if event.key == pygame.K_e:
                            level3 = True
                            levelscreenv = False




                 screen.fill(background_col1)
                 levelscreen.draw()

                 pygame.display.update()

                 clock.tick(FPS)

             if  level1:
                     #level1 = False
                     new_ground = Ground(1)
                     dist = 8
                     z = 10
                     HD = 10
                     HI = 50
                     OB  = 1
                     UF = 2
                     M = 10
                     B = 15

             if  level2:
                     #level2 = False
                     new_ground = Ground(2)
                     dist = 17
                     z = 8
                     HD = 15
                     HI = 40
                     OB  = 2
                     UF = 3
                     M = 12
                     B = 20



             if  level3:
                     #level3 = False
                     new_ground = Ground(2)
                     dist = 25
                     z = 7
                     HD = 20
                     HI = 30
                     OB  = 3
                     UF = 5
                     M = 25
                     B = 25




             while not gameOver:

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameOver = True

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_UP:
                                    if playerMan.rect.bottom == height - 100:
                                        playerMan.isJumping = True

                                        playerMan.movement[1] = -1*playerMan.jumpSpeed

                                """if event.key == pygame.K_DOWN:
                                    if not (playerMan.isJumping and playerMan.isDead):
                                        playerMan.isDucking = True"""


                                if event.key == pygame.K_SPACE:
                                    if playerMan.bullets >0:
                                        Bullets(playerMan.rect.right,playerMan.rect.centery,15,5)
                                        #gunshotM.play()
                                        playerMan.bullets -= 1
                                                                                                           #visit pygame.org/docs for any info on functions of pygame
                                if event.key == pygame.K_LEFT:
                                    if playerMan.rect.left > 0:
                                       playerMan.movingleft=True                                         # object moving L/R problem??????????????????????

                                if event.key == pygame.K_RIGHT:
                                    if playerMan.rect.right  < 900:
                                        playerMan.movingright=True


                                if event.key == pygame.K_c:
                                    if playerMan.missile > 0:
                                        Missile(playerMan.rect.top,playerMan.rect.centerx,11,20)
                                        playerMan.missile -= 1

                                pauses = True
                                if event.key == pygame.K_p:

                                    while pauses:

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                gameOver = True

                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_RETURN:
                                                    pauses = False

                                        displaytext("ENTER TO CONTINUE",100,width/2,height/2,(20,0,50))


                                        pygame.display.update()

                                        clock.tick(FPS)


                            if event.type == pygame.KEYUP:
                                if event.key == pygame.K_DOWN:
                                    playerMan.isDucking = False


                                if (event.key == pygame.K_LEFT or playerMan.rect.left < 0) :
                                    playerMan.movingleft=False

                                if (event.key == pygame.K_RIGHT or playerMan.rect.right > 900):
                                    playerMan.movingright=False


                        for c in obstacle:
                            if pygame.sprite.collide_mask(playerMan,c):
                                playerMan.isDead = True
                                playerMan.health = 0


                        for a in bombs:
                            if pygame.sprite.collide_mask(playerMan,a):
                                a.kill()
                                playerMan.health -= HD

                        for b in bullet:
                            for d in obstacle:
                                if pygame.sprite.collide_mask(b,d):
                                    b.kill()
                                    d.kill()
                                    Explode(b.rect.right,b.rect.centery,30,30)

                        for e in missiles:
                            for f in UFOs:
                                if pygame.sprite.collide_mask(e,f):
                                    e.kill()
                                    f.kill()
                                    playerMan.score += 20
                                    Explode(e.rect.centerx,e.rect.top,50,50)

                        for g in missiles:
                            for h in bombs:
                                if pygame.sprite.collide_mask(g,h):
                                    g.kill()
                                    h.kill()
                                    Explode(g.rect.centerx,g.rect.top,12,12)

                        for i in missilepack:
                            if pygame.sprite.collide_mask(playerMan,i):
                                playerMan.missile += M
                                i.kill()

                        for j in bulletpack:
                            if pygame.sprite.collide_mask(j,playerMan):
                                playerMan.bullets += B
                                j.kill()

                        for k in healthpack:
                            if pygame.sprite.collide_mask(k,playerMan):
                                k.kill()
                                playerMan.health += HI

                        for l in bombs:
                            for m in bullet:
                                if pygame.sprite.collide_mask(l,m):
                                    l.kill()
                                    m.kill()
                                    Explode(m.rect.right,m.rect.centery,12,12)

                        #cacti_spawn(counter)

                        if obstacleCounter%count == 0:
                            if len(obstacle) < OB :
                                Obstacles(35,80)

                        if ufocounter%countU == 0:
                            if len(UFOs) < UF:                                                   #NO OF OBSTACLE AND UFO
                                UFO(100,90)


                        if counterBM%1299 == 0:
                            if len(bulletpack)==0:
                                BulletPack()

                        if counterBM%599 == 0:
                            if len(missilepack)==0:
                                MissilePack()


                        if playerMan.health <= 0:
                            playerMan.isDead = True


                        """if playerMan.health <=20:
                            HealthPack()"""

                        if counterBM%2000 == 0:
                            HealthPack()


                        playerMan.update()                                           #https://github.com/shivamshekhar/PyGalaxian

                        obstacle.update()

                        new_ground.update(playerMan)

                        UFOs.update(playerMan,dist,z)

                        bullet.update()

                        bombs.update()

                        missiles.update()

                        missilepack.update()

                        bulletpack.update()
                        healthpack.update()
                        explode.update()


                        screen.fill(background_col)

                        new_ground.draw()

                        obstacle.draw(screen)

                        bulletpack.draw(screen)

                        missilepack.draw(screen)

                        playerMan.draw()

                        UFOs.draw(screen)

                        bullet.draw(screen)                                              #use  ?????????????????????????????????????//
                        bombs.draw(screen)
                        missiles.draw(screen)
                        missilebar.draw()
                        bulletbar.draw()
                        healthbar.draw()

                        healthpack.draw(screen)
                        explode.draw(screen)

                        displaytext("Score :" + str(playerMan.score),30,800,20,(20,0,50))

                        if level1:
                            displaytext("Level : 1",30,400,20,(20,0,50))

                        if level2:
                            displaytext("Level : 2",30,400,20,(20,0,50))

                        if level3:
                            displaytext("Level : 3",30,400,20,(20,0,50))



                        displaytext(" :" + str(playerMan.health) + "%",30,75,20,(50,0,20))
                        displaytext(": " + str(playerMan.bullets),30,width-65,60,(50,105,15))
                        displaytext(": " + str(playerMan.missile),30,70,60,(50,105,15))


                        pygame.display.update()

                        clock.tick(FPS)

                        if playerMan.isDead:
                            gameOver = True

                            #counters

                        obstacleCounter +=1
                        ufocounter += 1
                        count +=2
                        countU += 5


                        count = count%150+10
                        countU = countU%1189 +2
                        counter = (counter + 1)%1000000000
                        obstacleCounter = obstacleCounter%100000000000000 + 10
                        ufocounter =  ufocounter%10000000000
                        counterBM += 1



             while not gameExit:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            gameExit = True
                            gameOver = False
                            screen.fill(background_col)


                        if event.key == pygame.K_ESCAPE:
                            gameExit = True
                            gameOver = True
                            finalGameOver = True
                            startScreen = True



                """if HighScore < playerMan.score:
                        saveHighScore(playerMan.score)"""


                #screen.fill(background_col)
                exitscreen.draw()

                displaytext("Your Score :" + str(playerMan.score),70,width/2,height/2+80,(20,0,50))

                pygame.display.update()

                clock.tick(FPS)





    screen.fill(background_col)
    pygame.event.wait()

    pygame.quit()
    quit()






main()
