import settings as s
import math

class Player():

    def __init__(self, startposition, farbe):

        self.width = 40
        self.height = 20
        self.x = startposition[0]
        self.y = startposition[1]
        self.speed = 8
        self.colour = farbe

    def move(self,move_order):

        vx = move_order[0] - self.x
        vy = move_order[1] - self.y
        phi = math.atan2(vy,vx)

        if math.hypot(vx,vy) > 10:
        
            self.x += (math.cos(phi) * self.speed)
            self.y += (math.sin(phi) * self.speed)
        
            self.x = max(min(800 - (self.width // 2),self.x),(self.width // 2))
            self.y = max(min(600 - (self.height // 2),self.y),(self.height // 2))
        else: 
            self.x = self.x
            self.y = self.y



