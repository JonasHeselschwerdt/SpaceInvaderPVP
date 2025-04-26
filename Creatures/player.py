import settings as s
import pygame

class Player():

    def __init__(self, startposition):

        self.width = 40
        self.height = 20
        self.speed = 8
        self.colour = s.RED

    def move(self,move_x,move_y):

        self.x += move_x * self.speed
        self.y += move_y * self.speed
        self.x = max(0, min(s.WIDTH - self.width, self.x))
        self.y = max(0, min(s.HEIGHT - self.height, self.y))