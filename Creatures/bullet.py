import settings as s
import pygame

class Bullet():
        
    def __init__(self):

        self.x = 0
        self.y = 0
        self.width = 10
        self.height = 10
        self.speed = 10
        self.colour = s.BLUE
    
#    def spawn_bullet(self,player_x, player_y, player_width ):

#        return pygame.Rect(player_x + player_width // 2 - self.width // 2, player_y - self.height, self.width, self.height)