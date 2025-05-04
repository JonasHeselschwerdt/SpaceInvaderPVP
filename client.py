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

    shoot = False
    requestpause = False
    requestrestart = False
    requestcontinue = False
    requestshutdown = False

    for event in pygame.event.get():            
        if event.type == pygame.QUIT:           
            running = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_p:
                requestpause = True
            if event.key == pygame.K_r:
                requestrestart = True
            if event.key == pygame.K_c:
                requestcontinue = True
            if event.key == pygame.K_e:
                requestshutdown = True
                running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    input = {
        "MouseX": mouse_x ,
        "MouseY": mouse_y ,
        "shoot": shoot , 
        "requestpause" : requestpause,
        "requestrestart": requestrestart,
        "requestcontinue": requestcontinue,
        "requestshutdown": requestshutdown
        }

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

        bulletlist = player_info["Bulletlist"] 
        enemielist = player_info["Enemylist"]

        paused = player_info.get("Paused", False)
        spieler1leben = player_info.get("Spieler1Leben", 0)
        spieler2leben = player_info.get("Spieler2Leben", 0)

    except Exception as e:
        print(f"Fehler beim Empfangen: {e}")
        running = False

    pygame.draw.rect(window, Localplayercolour, (Localplayerx - 20, Localplayery - 10, 40, 20))
    pygame.draw.rect(window, Enemyplayercolour, (Enemyplayerx - 20, Enemyplayery - 10, 40, 20))

    for bullet in bulletlist:

        pygame.draw.rect(window,bullet.colour,(bullet.x,bullet.y,bullet.width,bullet.height))

    for enemy in enemielist:

        pygame.draw.rect(window,enemy.colour,(enemy.x,enemy.y,enemy.width,enemy.height))


#######

    leben_text_local = s.font.render(f"Blau: {spieler1leben if own_ip == player_info['PlayerIPs'][0] else spieler2leben} Leben", True, Localplayercolour)
    leben_text_enemy = s.font.render(f"Rot: {spieler2leben if own_ip == player_info['PlayerIPs'][0] else spieler1leben} Leben", True, Enemyplayercolour)

    window.blit(leben_text_local, (10, 10))
    window.blit(leben_text_enemy, (s.WIDTH - leben_text_enemy.get_width() - 10, 10))

# Pausenstatus anzeigen
    status_text = "PAUSIERT" if paused else "SPIEL LÄUFT"
    status_colour = s.YELLOW if paused else s.GREEN
    status_surface = s.font.render(status_text, True, status_colour)

    window.blit(status_surface, (s.WIDTH // 2 - status_surface.get_width() // 2, 10))

########

    pygame.display.flip()

pygame.quit()                                   
sys.exit()  