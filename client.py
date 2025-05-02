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

#sock.connect(('192.168.178.53', 65432))   # hier die IPv4 des PIs eingeben
#own_ip = sock.getsockname()[0]

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
    #sock.sendall(len(data).to_bytes(4, 'big') + data)
    sock.sendto(data, server_addr)

    # --- Daten vom Server empfangen ---
    try:
        # Erst die Länge lesen
        sock.settimeout(0.05)  # kurz warten
        try:
            data, _ = sock.recvfrom(4096)
            player_info = pickle.loads(data)
        except socket.timeout:
            continue  # falls kein Paket empfangen wurde
        """length_bytes = sock.recv(4)
        if not length_bytes:
            break  # Verbindung verloren
        length = int.from_bytes(length_bytes, 'big')

        # Dann die eigentlichen Daten lesen
        received_data = b''
        while len(received_data) < length:
            packet = sock.recv(length - len(received_data))
            if not packet:
                break
            received_data += packet

        player_info = pickle.loads(received_data)"""

        if own_ip == player_info["PlayerIPs"][0]:
            Localplayercolour = player_info["colour1"]
            Localplayerx = player_info["x1"]
            Localplayery = player_info["y1"]
            #Enemyplayercolour = player_info["colour2"]
            #Enemyplayerx = player_info["x2"]
            #Enemyplayery = player_info["y2"]
        else:
            #Localplayercolour = player_info["colour2"]
            #Localplayerx = player_info["x2"]
            #Localplayery = player_info["y2"]
            Enemyplayercolour = player_info["colour1"]
            Enemyplayerx = player_info["x1"]
            Enemyplayery = player_info["y1"]
        
    except Exception as e:
        print(f"Fehler beim Empfangen: {e}")
        running = False

    pygame.draw.rect(window, Localplayercolour, (Localplayerx - 20, Localplayery - 10, 40, 20))
    #pygame.draw.rect(window, Enemyplayercolour, (Enemyplayerx - 20, Enemyplayery - 10, 40, 20))

    pygame.display.flip()

pygame.quit()                                   
sys.exit()  