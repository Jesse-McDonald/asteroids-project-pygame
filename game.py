from __future__ import print_function,division
from pygame import *
from math import *
from random import *


init()
HEIGHT = 500 
WIDTH = 600
display.set_caption('Asteroids')
screen = display.set_mode((WIDTH, HEIGHT))
tfont = font.Font(None, 36)
def sqr(x):
    return x*x
class Player:

    def __init__(self):
        self.sprite = image.load("ship.png")
        self.spriteO=self.sprite
        self.rect = self.sprite.get_rect()
        self.vel=[0,0]
        self.pos=[WIDTH/2,HEIGHT/2]
        self.rot=pi/2
        self.rotV=0
        self.deathtime=100
    def velCalc(self):
        self.vel[0]-=sin(self.rot)*0.1
        self.vel[1]-=cos(self.rot)*0.1
        #self.vel=(cos(self.rot),sin(self.rot))
    def update_and_display(self):
        self.deathtime-=1
        self.rot+=self.rotV
        centerx=self.rect.centerx
        centery=self.rect.centery
        self.sprite=transform.rotate(self.spriteO,self.rot/(pi)*180)
        self.rect = self.sprite.get_rect()
        self.rect.centerx=centerx
        self.rect.centery=centery
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1]     
        screen.blit(self.sprite, self.rect)
    def teleport(self):
        self.vel=[0,0]
        self.rotV=0
        self.pos=[random()*WIDTH,random()*HEIGHT]
    def kill(self):
        if self.deathtime<0:
            global deaths
            deaths-=1
            self.__init__()
class bullet:
    age=1000
    def __init__(self,pos,direction):
        self.pos=pos
        self.vel=[sin(direction)*10,cos(direction)*10]
        self.age=40
        self.sprite = image.load("bullet.png")
        self.rect = self.sprite.get_rect()
    def update(self):
        self.age-=1
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        self.pos[1]%=HEIGHT
        self.pos[0]%=WIDTH
        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1]
        screen.blit(self.sprite, self.rect)
class Asteroid:
    def __init__(self,pos,size,vel):
        self.sprite = image.load("asteroid.png")
        self.rect = self.sprite.get_rect()
        size_of=[self.sprite.get_size()[0]*size*2,self.sprite.get_size()[1]*2*size]
        self.sprite=transform.scale(self.sprite, size_of)
        self.spriteO=self.sprite
        
        self.vel=vel
        self.pos=pos
        self.rot=pi/2
        self.rotV=random()*10
        self.size=size
    def update_and_display(self):
        self.rot+=self.rotV
        centerx=self.rect.centerx
        centery=self.rect.centery
        self.sprite=transform.rotate(self.spriteO,self.rot/(pi)*180)
        self.rect = self.sprite.get_rect()
        self.rect.centerx=centerx
        self.rect.centery=centery
        self.pos[0]+=self.vel[0]/self.size
        self.pos[1]+=self.vel[1]/self.size
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1]     
        screen.blit(self.sprite, self.rect)
    def collide(self,target,mod=0):
        distance=sqrt(sqr(self.rect.centerx-target.rect.centerx)+sqr(self.rect.centery-target.rect.centery))
        return distance <=20*self.size+mod
from time import sleep
player=Player()
FORWARD=False
LEFT=False
RIGHT=False
bullets=[]
astro=4
asteroids=[Asteroid([random()*WIDTH,random()*HEIGHT],3,[2*random()-1,2*random()-1]) for i in range(astro)]
score=0
deaths=3
def astroHit(asteroids,i):
    global score
    if asteroids[i].size>1:
        asteroids.append(Asteroid([asteroids[i].pos[0],asteroids[i].pos[1]], asteroids[i].size-1,[2*random()-1,2*random()-1]))
        asteroids[i]=(Asteroid(asteroids[i].pos, asteroids[i].size-1,[2*random()-1,2*random()-1]))
    else:
        asteroids.remove(asteroids[i])
    score+=10
def gameover(score):
    global WIDTH, HEIGHT
    while True:
        screen.fill((0,0,0))
        text = tfont.render("Game Over", 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.center=[WIDTH/2,HEIGHT/2]
        screen.blit(text, textpos)
        text = tfont.render("Your score was: "+str(score), 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.center=[WIDTH/2,HEIGHT/2+30]
        screen.blit(text, textpos)
        display.flip()
        sleep(0.01)
while True:
    if deaths <1:
        gameover(score)
    #bullets.append(bullet([player.pos[0],player.pos[1]],player.rot+pi))#debug lazer
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_w:
                FORWARD=True
            if e.key == K_a:
                LEFT=True
            if e.key == K_d:
                RIGHT=True
            if e.key == K_s:
                player.teleport()
                player.deathtime=10
            if e.key == K_SPACE:
                bullets.append(bullet([player.pos[0],player.pos[1]],player.rot+pi))
        if e.type == QUIT:
            from sys import exit
            exit()
        if e.type==KEYUP:
            if e.key ==K_w:
                FORWARD=False
            if e.key == K_a:
                LEFT=False
            if e.key == K_d:
                RIGHT=False
    if FORWARD:

        player.velCalc()
    if LEFT:
        player.rotV+=0.0005
    if RIGHT:
        player.rotV-=0.0005
    screen.fill((0,0,0))
    player.update_and_display()
    i=0
    if len(asteroids)<1:
        deaths+=1
        astro+=2
        asteroids=[Asteroid([random()*WIDTH,random()*HEIGHT],3,[2*random()-1,2*random()-1]) for i in range(astro)]
        player.deathtime=100
    while i<len(asteroids):
        deathflag=False
        asteroids[i].update_and_display()
        if asteroids[i].collide(player,10):
            deathflag=True
            player.kill()
        j=0
        while j<len(bullets):
            if not(i<len(asteroids)):
                i=len(asteroids)-1
                i=min(0,i)
            if asteroids[i].collide(bullets[j]):
                #print("colide")
                deathflag=True
                bullets.remove(bullets[j])
            j+=1
        if deathflag:
            astroHit(asteroids,i)
        i+=1
        
    if len(bullets)>0:
        i=0
        while i < len(bullets):
            bullets[i].update()
            if bullets[i].age<0:
                bullets.remove(bullets[i])
            i+=1
    text = tfont.render("Score: "+str(score), 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.left= 10
    textpos.top = 10
    screen.blit(text, textpos)
    text = tfont.render("Lives: "+str(deaths), 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.left= 10
    textpos.top = 35
    screen.blit(text, textpos)
    display.flip()
    sleep(0.01)

