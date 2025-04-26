import pygame            
import sys                              
import socket                          
import pickle                                
import settings as s
from Creatures import *

pygame.init()
window = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption("Space Invader PVP") 
clock = pygame.time.Clock() 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
sock.connect(('192.168.0.133', 65432))   # hier die IPv4 des PIs eingeben

Localplayer = Player((0,0))
Enemyplayer = Player((0,0))
Localplayer.colour = s.BLUE
Enemyplayer.colour  = s.RED

running = True

while running:

    clock.tick(60)
    window.fill(s.BLACK) 

    for event in pygame.event.get():            
        if event.type == pygame.QUIT:           
            running = False  
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        shoot = True
    else:
        shoot = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    input = {"MouseX": mouse_x , "MouseY": mouse_y , "shoot": shoot}

    data = pickle.dumps(input)
    sock.sendall(len(data).to_bytes(4, 'big') + data)

pygame.quit()                                   
sys.exit()  