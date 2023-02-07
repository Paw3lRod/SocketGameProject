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
player2 = Player("jeremy", 0, 0)
sprites.append(player1)
sprites.append(player2)

# Main loop for the Pygame window
running = True
while running:
    # update from server
    data = client_socket.recv(4096)
    decoded_data = pickle.loads(data)

    screen.fill(decoded_data["color"])
    player1.x = decoded_data["player1_data"]["x"]
    player1.y = decoded_data["player1_data"]["y"]
    player2.x = decoded_data["player2_data"]["x"]
    player2.y = decoded_data["player2_data"]["y"]

    selected_player = player1
    selected_data = "player1_data"

    if decoded_data["user"] == "2":
        selected_player = player2
        selected_data = "player2_data"

    # blit sprites
    for sprite in sprites:
        screen.blit(sprite.image, (sprite.x, sprite.y))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                decoded_data['pressed_key'] = "l"
        if event.type == pygame.QUIT:
            running = False

        # inputs
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            selected_player.y -= selected_player.velocity
        if keys[pygame.K_DOWN]:
            selected_player.y += selected_player.velocity
        if keys[pygame.K_RIGHT]:
            selected_player.x += selected_player.velocity
        if keys[pygame.K_LEFT]:
            selected_player.y -= selected_player.velocity

    pygame.display.update()

    # send updates to server
    decoded_data[selected_data]["x"] = selected_player.x
    decoded_data[selected_data]["y"] = selected_player.y

    package = pickle.dumps(decoded_data)
    client_socket.sendall(package)

# Close the socket connection and Pygame
client_socket.close()
pygame.quit()
