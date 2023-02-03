# server.py
import socket
import pickle
import pygame
import threading

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

# Initialize Pygame
pygame.init()

# Accept a connection from a client
clients = []
while len(clients) < 2:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)

main_data = {"color": (0, 0, 0), "pressed_key": "",
             "player1": {}, "player2": {}, "sprites": []}
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

    for client_data in decoded_data:
        sprites += client_data["sprites"]

        if client_data["pressed_key"] == "w":
            if client_data['color'] == (255, 255, 255):
                main_data['color'] = (0, 0, 0)
            else:
                main_data['color'] = (255, 255, 255)
            main_data["pressed_key"] = ""

    main_data["sprites"] = sprites

    package = pickle.dumps(main_data)
    for client_socket in clients:
        client_socket.sendall(package)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


client_socket.close()
server_socket.close()
pygame.quit()
