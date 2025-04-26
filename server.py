import socket
import pickle

# Server-Adresse und Port
HOST = '0.0.0.0'  # Lausche auf allen Netzwerk-Interfaces
PORT = 65432      # Gleicher Port wie im Client

# TCP/IP-Socket erstellen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(2)  # Maximal 2 Clients gleichzeitig (für später wichtig)
print(f"Server läuft auf {HOST}:{PORT} und wartet auf Verbindung...")

# Verbindung akzeptieren
conn, addr = server_socket.accept()
print(f"Verbunden mit {addr}")

# Nachrichten empfangen
try:
    while True:

        length_bytes = conn.recv(4)
        length = int.from_bytes(length_bytes, 'big')
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                break
            data += packet
        obj = pickle.loads(data)
        print(f"Empfangen: {obj}")

finally:
    conn.close()
    server_socket.close()
