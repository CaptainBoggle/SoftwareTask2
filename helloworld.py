import pygame
from pygame.locals import *
import os
import sys

pygame.init()

screen = pygame.display.set_mode((900,580))
clock=pygame.time.Clock()

bg1 = pygame.image.load(os.path.join("mapideas", "meadow.png"))
bg2 = pygame.image.load(os.path.join("mapideas", "rake.png"))

ts1 = pygame.image.load(os.path.join("towers", "drafts","t1.png")).convert_alpha()
ts2 = pygame.image.load(os.path.join("towers", "drafts","t1o.png")).convert_alpha()
ts3 = pygame.image.load(os.path.join("towers", "drafts","t2.png")).convert_alpha()
ts4 = pygame.image.load(os.path.join("towers", "drafts","t2o.png")).convert_alpha()
bg = bg1

class Tower(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=pos)

class AI(object):
    def __init__(self,x,y,speed):
        self.x=x
        self.y=y
        self.speed = speed
        self.path=[(444,246),(444,114),(294,114),(294,462),(150,460),(150,340),(570,340),(570,200),(674,200),(674,414),(400,414),(400,574)]
    def update(self):
        if not self.path:
           return
        if self.x<(self.path[0])[0]:
            self.x+=self.speed
        if self.x>(self.path[0])[0]:
            self.x-=self.speed
        if self.y<(self.path[0])[1]:
            self.y+=self.speed
        if self.y>(self.path[0])[1]:
            self.y-=self.speed
        z=(self.x-(self.path[0])[0],self.y-(self.path[0])[1])
        if (z[0]/-self.speed,z[1]/-self.speed)==(0,0):
            self.path=self.path[1:]
        pygame.draw.circle(screen,((255,0,0)),(self.x,self.y),3,0)





enemies = [AI(0,240,)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if bg == bg1:
                bg = bg2
            else: bg = bg1

    pygame.display.set_caption(str(pygame.mouse.get_pos()))

            

    screen.fill((255,255,255))
    screen.blit(bg, (0,0))
    for e in enemies:
    	e.update()

    clock.tick(60)
    pygame.display.flip()