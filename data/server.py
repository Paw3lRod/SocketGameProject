# server.py
import socket
import pickle
import pygame
from player import Player

# ticks
last_processed_input = {"1": 0, "2": 0}

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen()

# Initialize Pygame
pygame.init()

# Accept two connections from clients
clients = []
while len(clients) < 2:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)

main_data = {
    "user": "",
    "color": (255, 255, 255),
    "pressed_key": "",
    "player1_data": {
        "key_downs": [],
        "key_ups": [],
        "timestamp": 0,
    },
    "player2_data": {
        "key_downs": [],
        "key_ups": [],
        "timestamp": 0,
    },
}
package = pickle.dumps(main_data)

for client_socket in clients:
    client_socket.sendall(package)


# Main loop for the Pygame window
running = True
while running:
    # receive updates
    sprites = []
    decoded_data = []
    for client_socket in clients:
        data = client_socket.recv(4096)
        if data:
            decoded_data.append(pickle.loads(data))

    for i in range(len(decoded_data)):
        nr = str(i + 1)

        if decoded_data[i][f"player{nr}_data"]["timestamp"] > last_processed_input[nr]:
            main_data[f"player{nr}_data"]["key_downs"] = decoded_data[i][
                f"player{nr}_data"
            ]["key_downs"]
            main_data[f"player{nr}_data"]["key_ups"] = decoded_data[i][
                f"player{nr}_data"
            ]["key_ups"]

            last_processed_input[nr] = decoded_data[i][f"player{nr}_data"]["timestamp"]

    # send updates to clients
    player1_data = {}
    player1_data.update(main_data)
    player2_data = {}
    player2_data.update(main_data)

    player1_data["user"] = "1"
    player2_data["user"] = "2"
    package1 = pickle.dumps(player1_data)
    package2 = pickle.dumps(player2_data)

    clients[0].sendall(package1)
    clients[1].sendall(package2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


client_socket.close()
server_socket.close()
pygame.quit()
