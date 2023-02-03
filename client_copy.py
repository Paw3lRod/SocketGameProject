# client.py
import socket
import pickle
import pygame

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))

# Create and send a package to the server


# Main loop for the Pygame window
running = True
while running:
    data = client_socket.recv(4096)
    decoded_data = pickle.loads(data)
    screen.fill(decoded_data["color"])

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                decoded_data['pressed_key'] = "w"
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

    package = pickle.dumps(decoded_data)
    client_socket.sendall(package)

# Close the socket connection and Pygame
client_socket.close()
pygame.quit()
