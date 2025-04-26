import settings as s
import random
import pygame

class Normal_Enemy():

    def __init__(self):

        self.x = 0
        self.y = 0
        self.colour = s.WHITE
        self.speed = 2
        self.width = 30
        self.height = 30
        self.points = 1

#    def spawn_random(self):

#        self.x = random.randint(0, config.WIDTH - self.width)
#        return pygame.Rect(self.x, 0, self.width, self.height)

    def setRandomSpawn(self):
        self.x = random.randint(0,s.WIDTH - self.width)