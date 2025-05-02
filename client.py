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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

server_addr = ('192.168.178.53', 65432)
own_ip = socket.gethostbyname(socket.gethostname())

running = True

Localplayercolour = s.BLUE
Localplayerx = 0
Localplayery = 0
Enemyplayerx = 0
Enemyplayery = 0
Enemyplayercolour = s.RED

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
    sock.sendto(data, server_addr)

    try:
        sock.settimeout(0.05)
        try:
            data, _ = sock.recvfrom(4096)
            player_info = pickle.loads(data)
        except socket.timeout:
            continue  

        if own_ip == player_info["PlayerIPs"][0]:
            Localplayercolour = player_info["colour1"]
            Localplayerx = player_info["x1"]
            Localplayery = player_info["y1"]
            Enemyplayercolour = player_info["colour2"]
            Enemyplayerx = player_info["x2"]
            Enemyplayery = player_info["y2"]
        else:
            Localplayercolour = player_info["colour2"]
            Localplayerx = player_info["x2"]
            Localplayery = player_info["y2"]
            Enemyplayercolour = player_info["colour1"]
            Enemyplayerx = player_info["x1"]
            Enemyplayery = player_info["y1"]
        
    except Exception as e:
        print(f"Fehler beim Empfangen: {e}")
        running = False

    pygame.draw.rect(window, Localplayercolour, (Localplayerx - 20, Localplayery - 10, 40, 20))
    pygame.draw.rect(window, Enemyplayercolour, (Enemyplayerx - 20, Enemyplayery - 10, 40, 20))

    pygame.display.flip()

pygame.quit()                                   
sys.exit()  