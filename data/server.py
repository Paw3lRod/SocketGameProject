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
    "player1_data": {"x": 0, "y": 0, "direction": "down", "timestamp": 0},
    "player2_data": {"x": 0, "y": 0, "direction": "down", "timestamp": 0},
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
        # makes player1 control player1 and player2 control player2
        if i == 0:
            if decoded_data[i]["player1_data"]["timestamp"] > last_processed_input["1"]:
                main_data["player1_data"]["x"] = decoded_data[i]["player1_data"]["x"]
                main_data["player1_data"]["y"] = decoded_data[i]["player1_data"]["y"]
                main_data["player1_data"]["direction"] = decoded_data[i][
                    "player1_data"
                ]["direction"]

                last_processed_input["1"] = decoded_data[i]["player1_data"]["timestamp"]

        elif i == 1:
            if decoded_data[i]["player2_data"]["timestamp"] > last_processed_input["2"]:
                main_data["player2_data"]["x"] = decoded_data[i]["player2_data"]["x"]
                main_data["player2_data"]["y"] = decoded_data[i]["player2_data"]["y"]
                main_data["player2_data"]["direction"] = decoded_data[i][
                    "player2_data"
                ]["direction"]

                last_processed_input["2"] = decoded_data[i]["player2_data"]["timestamp"]

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
