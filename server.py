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
        data = conn.recv(2048)  # Größere Puffergröße, falls nötig
        if not data:
            break  # Verbindung wurde geschlossen
        input_data = pickle.loads(data)
        print(f"Empfangen: {input_data}")
finally:
    conn.close()
    server_socket.close()
