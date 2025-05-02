import socket
import pickle
import threading
import settings as s
from Creatures import Player
import time

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

Player1 = Player((s.WIDTH // 2, s.HEIGHT - 40),s.BLUE)
#Player2 = Player((s.WIDTH // 2 , 40),s.RED)

while True:

    start_time = time.time()
    
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
    except socket.timeout:
        pass

    try:
        player1move = (playerinput[0]["MouseX"], playerinput[0]["MouseY"])
        #player2move = (playerinput[1]["MouseX"], playerinput[1]["MouseY"])
    except:
        player1move = (0,0)
        #player2move = (0,0)

    Player1.move(player1move)
    #Player2.move(player2move)

    daten = {
        "x1": Player1.x,
        "y1": Player1.y,
        "colour1": Player1.colour,
        #"x2": Player2.x,
        #"y2": Player2.y,
        #"colour2":Player2.colour,
        "PlayerIPs": player_ips
    }

    data_serialized = pickle.dumps(daten)
    data_length = len(data_serialized).to_bytes(4, 'big')

    for addr in player_addresses.values():
        server_socket.sendto(data_serialized, addr)

    elapsed_time = time.time() - start_time
    time_to_sleep = max(0,1/60 - elapsed_time)
    time.sleep(time_to_sleep)



    




