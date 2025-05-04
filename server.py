import socket
import pickle
import settings as s
from Creatures import Player
from Creatures import Bullet
from Creatures import Normal_Enemy
import time
import pygame
import random
import sys

pygame.init()

HOST = '0.0.0.0'  
PORT = 65432     

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

connections = []
playerinput = {}
player_ips = []
 
print(f"Server läuft auf {HOST}:{PORT} und wartet auf Verbindung...")

player_addresses = {}
playerinput = {}

Player1 = Player((s.WIDTH // 2, s.HEIGHT - 80),s.BLUE,1)
Player2 = Player((s.WIDTH // 2 , 80),s.RED,2)
bullets = []
enemies = []
paused = False

running = True

while running:

    start_time = time.time()

    ##### 

    try:
        server_socket.settimeout(0.01)
        while True:
            data, addr = server_socket.recvfrom(4096)
            input_data = pickle.loads(data)

            if addr not in player_addresses.values():
                player_id = len(player_addresses)
                player_addresses[player_id] = addr
                player_ips.append(addr[0])
                print(f"Spieler {player_id} verbunden: {addr}")

            player_id = [k for k, v in player_addresses.items() if v == addr][0]
            playerinput[player_id] = input_data

            if input_data.get("requestpause"):
                paused = True
            if input_data.get("requestcontinue") and not (Player1.lives * Player2.lives == 0):
                paused = False
            if input_data.get("requestrestart"):
                bullets.clear()
                enemies.clear()
                Player1.x = 0
                Player1.y = 0
                Player2.x = 0
                Player2.y = 0
                Player1.lives = 5
                Player2.lives = 5
                paused = False
            if input_data.get("requestshutdown"):
                bullets.clear()
                enemies.clear()
                Player1.x = 0
                Player1.y = 0
                Player2.x = 0
                Player2.y = 0
                Player1.lives = 5
                Player2.lives = 5
                running = False

    except socket.timeout:
        pass
        
    #####
    if not paused:

        try:
            player1move = (playerinput[0]["MouseX"], playerinput[0]["MouseY"])
            player2move = (playerinput[1]["MouseX"], playerinput[1]["MouseY"])
        except:
            pass

        try:
            Player1.move(player1move)
            Player2.move(player2move)
        except:
            pass
        try:
            if playerinput[0]["shoot"] == True:
                bullets.append(Bullet((Player1.x,Player1.y),1,s.LBLUE))

            if playerinput[1]["shoot"] == True:
                bullets.append(Bullet((Player2.x,Player2.y),2,s.LRED))
        
        except:
            pass

        for bullet in bullets:
            bullet.movebullet()

            if bullet.player == 1:
                playerrect = Player2.rect
            elif bullet.player == 2:
                playerrect = Player1.rect
            
            if bullet.rect.colliderect(playerrect):
                bullet.delete = True
                if bullet.player == 1:
                    Player2.lives -= 1
                    print(f"Player 2 has now {Player2.lives} lives left")
                elif bullet.player == 2:
                    Player1.lives -= 1
                    print(f"player 1 now has {Player1.lives} lives left")


        if random.random() < (s.SPAWNPROB / 60):

            new_enemy = Normal_Enemy()
            new_enemy.assignrandomspeed()
            enemies.append(new_enemy)
        
        for enemy in enemies:

            enemy.moveenemy()
            
            if enemy.rect.colliderect(Player1.rect):
                Player1.lives -= 1
                enemy.delete = True
            elif enemy.rect.colliderect(Player2.rect):
                Player2.lives -= 1
                enemy.delete = True

            for bullet in bullets:

                if bullet.rect.colliderect(enemy.rect):
                    bullet.delete = True

        enemies = [enemy for enemy in enemies if 0 <= enemy.y <= s.HEIGHT and 0 <= enemy.x <= s.WIDTH and not enemy.delete]
        bullets = [bullet for bullet in bullets if 0 <= bullet.y <= s.HEIGHT and not bullet.delete]

        if (Player1.lives * Player2.lives) == 0:
            paused = False
        
    daten = {
        "x1": Player1.x,
        "y1": Player1.y,
        "colour1": Player1.colour,
        "x2": Player2.x,
        "y2": Player2.y,
        "colour2":Player2.colour,
        "PlayerIPs": player_ips,
        "Bulletlist": bullets,
        "Enemylist": enemies,
        "Spieler1Leben": Player1.lives,
        "Spieler2Leben": Player2.lives,
        "Paused": paused
    }

    data_serialized = pickle.dumps(daten)
    data_length = len(data_serialized).to_bytes(4, 'big')

    for addr in player_addresses.values():
        server_socket.sendto(data_serialized, addr)

    elapsed_time = time.time() - start_time
    time_to_sleep = max(0,1/60 - elapsed_time)
    time.sleep(time_to_sleep)

pygame.quit()
sys.exit()



    




