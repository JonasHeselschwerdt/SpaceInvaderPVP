import settings as s
import pygame

class Bullet():
        
    def __init__(self,position,playertype,colour):

        self.x = position[0]
        self.y = position[1]
        self.width = 10
        self.height = 10
        self.speed = 10
        self.colour = colour
        self.player = playertype
        self.delete = False
    
    def movebullet(self):
        
        if self.player == 1:
            self.y -= self.speed
        elif self.player == 2:
            self.y += self.speed