import socket
import pickle
import threading
import settings as s
from Creatures import Player
import time

HOST = '0.0.0.0'  
PORT = 65432     


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

connections = []
playerinput = {}

# Threading starten:

def client_thread(conn, spieler_id): 
    
    global playerinput
    try:
        while True:
            start_time = time.time()
            length_bytes = conn.recv(4)
            length = int.from_bytes(length_bytes, 'big')
            data = b''
            while len(data) < length:
                packet = conn.recv(length - len(data))
                if not packet:
                    break
                data += packet
            inp = pickle.loads(data)
            playerinput[spieler_id] = inp
            #print(playerinput)
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0,1/60 - elapsed_time)
            time.sleep(time_to_sleep)
    finally:
        conn.close()
        #server_socket.close()



server_socket.listen(2)  
print(f"Server läuft auf {HOST}:{PORT} und wartet auf Verbindung...")

playercounter = 0
while playercounter < 2:

    conn, addr = server_socket.accept()
    print(f"Verbunden mit {addr}")
    connections.append(conn)
    thread = threading.Thread(target=client_thread, args=(conn, playercounter))
    thread.start()
    playercounter += 1

# Ab hier Gameloop:

Player1 = Player((s.WIDTH // 2, s.HEIGHT - 40),s.BLUE)
Player2 = Player((s.WIDTH // 2 , 40),s.RED)

while True:
    start_time = time.time()
    try:

        player1move = (playerinput[0]["MouseX"], playerinput[0]["MouseY"])
        #print(player1move)
        player2move = (playerinput[1]["MouseX"], playerinput[1]["MouseY"])

    except:

        player1move = (0,0)
        player2move = (0,0)

    Player1.move(player1move)
    Player2.move(player2move)

    daten1 = {
        "x": Player1.x,
        "y": Player1.y,
        "colour": Player1.colour
    }

    data_serialized = pickle.dumps(daten1)
    data_length = len(data_serialized).to_bytes(4, 'big')

    for conn in connections:
        try:
            conn.sendall(data_length + data_serialized)
        except:
            pass
    elapsed_time = time.time() - start_time
    time_to_sleep = max(0,1/60 - elapsed_time)
    time.sleep(time_to_sleep)



    




