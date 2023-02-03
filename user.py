# client.py
import socket
import pickle
import pygame
from player import Player

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))

# Create and send a package to the server
sprites = []
player1 = Player("jeremy", 0, 0)
sprites.append(player1)

# Main loop for the Pygame window
running = True
while running:
    # update from server
    data = client_socket.recv(4096)
    decoded_data = pickle.loads(data)

    server_sprites = decoded_data["sprites"]

    for sprite in server_sprites:
        decoded_image = pygame.image.fromstring(
            sprite.image, (115, 115), 'RGBA')
        screen.blit(decoded_image, sprite.pos)

    screen.fill(decoded_data["color"])

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                decoded_data['pressed_key'] = "w"
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

    # client updates
    decoded_data["sprites"] = []
    # for sprite in sprites:
    #     decoded_data["sprites"].append(
    #         {"image": sprite.surface_string, "pos": (sprite.x, sprite.y)})

    package = pickle.dumps(decoded_data)
    client_socket.sendall(package)

# Close the socket connection and Pygame
client_socket.close()
pygame.quit()
