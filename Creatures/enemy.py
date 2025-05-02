import settings as s
import random
import math
import pygame

class Normal_Enemy():

    def __init__(self):

        self.x = random.choice([0,s.WIDTH])
        self.y = random.randint(100,s.HEIGHT - 100)
        self.colour = s.WHITE
        self.speedabs = 2
        self.speedy = 0
        self.speedx = 0
        self.width = 30
        self.height = 30
        self.delete = False
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def assignrandomspeed(self):

        if self.x == 0:
            rPhi = random.randint(-30,30)
            self.speedx = math.cos(math.radians(rPhi)) * self.speedabs
            self.speedy = math.sin(math.radians(rPhi)) * self.speedabs
        elif self.x == s.WIDTH:
            rPhi = random.randint(-150,150)
            self.speedx = math.cos(math.radians(rPhi)) * self.speedabs
            self.speedy = math.sin(math.radians(rPhi)) * self.speedabs

    def moveenemy(self):

        self.x += self.speedx * self.speedabs
        self.y += self.speedy * self.speedabs
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)




