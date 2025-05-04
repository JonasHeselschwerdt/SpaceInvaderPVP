import settings as s
import math
import pygame

class Player():

    def __init__(self, startposition, farbe, typ):

        self.width = 40
        self.height = 20
        self.x = startposition[0]
        self.y = startposition[1]
        self.speed = 8
        self.colour = farbe
        self.type = typ
        self.lives = 5
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def move(self,move_order):

        vx = move_order[0] - self.x
        vy = move_order[1] - self.y
        phi = math.atan2(vy,vx)

        if math.hypot(vx,vy) > 10:
        
            self.x += (math.cos(phi) * self.speed)
            self.y += (math.sin(phi) * self.speed)
        
            self.x = max(min(800 - (self.width // 2),self.x),(self.width // 2))
            if self.type == 1:
                self.y = max(min(550 - (self.height // 2),self.y),400 - (self.height // 2))
            elif self.type == 2:
                self.y = max(min(200 - (self.height // 2),self.y), 50 + (self.height // 2)) 
                           
        else: 
            self.x = self.x
            self.y = self.y

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)



