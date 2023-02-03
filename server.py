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
client_socket, client_address = server_socket.accept()
clients = []
clients.append(client_socket)
data = {"color": (0, 0, 0), "pressed_key": ""}
package = pickle.dumps(data)

for client_socket in clients:
    client_socket.send(package)


# Main loop for the Pygame window
running = True
while running:
    for client_socket in clients:
        data = client_socket.recv(4096)

    decoded_data = pickle.loads(data)
    if decoded_data["pressed_key"] == "w":
        if decoded_data['color'] == (255, 255, 255):
            decoded_data['color'] = (0, 0, 0)
        else:
            decoded_data['color'] = (255, 255, 255)
        decoded_data["pressed_key"] = ""

    package = pickle.dumps(decoded_data)
    client_socket.sendall(package)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


client_socket.close()
server_socket.close()
pygame.quit()
