import pygame
import sys
import socket
import pickle
from data.button import draw_button_list
from data.button import Button
from data.counter import Counter
from data.player import Player


class Game_manager:
    def __init__(self, screen, fps) -> None:
        self.screen = screen
        self.fps = fps
        self.state = self.intro_menu
        self.clock = pygame.time.Clock()

    def intro_menu(self):
        button_play = Button(200, 60, "Play online", 26, (255, 112, 150), (0, 0))
        button_customize = Button(200, 60, "Customize", 26, (255, 112, 150), (0, 0))
        button_practice = Button(200, 60, "Practice", 26, (255, 112, 150), (0, 0))
        buttons = [button_customize, button_play, button_practice]
        selected_button = Counter(len(buttons), 0)

        while True:
            # blit
            self.screen.fill((255, 255, 255))
            draw_button_list(
                buttons, selected_button, self.screen, space=250, pos=(150, 500)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    selected_button.dec()
                if keys[pygame.K_RIGHT]:
                    selected_button.inc()
                if keys[pygame.K_RETURN]:
                    if button_practice.selected:
                        self.practice_field()
                    elif button_play.selected:
                        self.load_online()

            self.clock.tick(self.fps)
            pygame.display.update()

    def practice_field(self):
        sprites = []
        player1 = Player("blue", 0, 0)
        player2 = Player("red", 420, 100)
        player1.change_velocity(1)
        sprites.append(player1)
        sprites.append(player2)

        # Main loop for the Pygame window
        running = True
        while running:
            # update from server
            self.screen.fill((255, 255, 255))
            selected_player = player1

            # blit sprites
            for sprite in sprites:
                self.screen.blit(sprite.image, (sprite.x, sprite.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

                # inputs
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_player.move(0, -1, "start")
                    if event.key == pygame.K_DOWN:
                        selected_player.move(0, 1, "start")
                    if event.key == pygame.K_RIGHT:
                        selected_player.move(1, 0, "start")
                    if event.key == pygame.K_LEFT:
                        selected_player.move(-1, 0, "start")
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        selected_player.move(0, -1, "stop")
                    if event.key == pygame.K_DOWN:
                        selected_player.move(0, 1, "stop")
                    if event.key == pygame.K_RIGHT:
                        selected_player.move(1, 0, "stop")
                    if event.key == pygame.K_LEFT:
                        selected_player.move(-1, 0, "stop")

                # diagonal direction control
                keys = pygame.key.get_pressed()
                if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                    selected_player.vel_y = 0
                if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                    selected_player.vel_x = 0

            player1.update()
            player2.update()

            pygame.display.update()

    def load_online(self):
        loading_text = pygame.font.SysFont("arial", 40).render(
            "Connecting to server...", True, (255, 255, 255)
        )

        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except:
                pass

            self.screen.fill((0, 0, 0))
            self.screen.blit(loading_text, (200, 300))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

            try:
                client_socket.connect(("127.0.0.1", 12345))
            except:
                continue
            else:
                break

        # - -- -- - - - - -ter succesfull connection - -- -- - - - - - - -
        sprites = []
        player1 = Player("jeremy", 0, 0)
        player2 = Player("jeremy", 0, 0)
        sprites.append(player1)
        sprites.append(player2)

        running = True
        # Main loop for the Pygame window
        while running:
            # update from server
            data = client_socket.recv(4096)
            decoded_data = pickle.loads(data)

            self.screen.fill(decoded_data["color"])
            player1.x = decoded_data["player1_data"]["x"]
            player1.y = decoded_data["player1_data"]["y"]
            player1.turn(decoded_data["player1_data"]["direction"])

            player2.x = decoded_data["player2_data"]["x"]
            player2.y = decoded_data["player2_data"]["y"]
            player2.turn(decoded_data["player2_data"]["direction"])

            selected_player = player1
            selected_data = "player1_data"

            if decoded_data["user"] == "2":
                selected_player = player2
                selected_data = "player2_data"

            # blit sprites
            for sprite in sprites:
                self.screen.blit(sprite.image, (sprite.x, sprite.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # inputs
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_player.vel_y += -selected_player.velocity
                        selected_player.turn("up")
                    if event.key == pygame.K_DOWN:
                        selected_player.vel_y += selected_player.velocity
                        selected_player.turn("down")
                    if event.key == pygame.K_RIGHT:
                        selected_player.vel_x += selected_player.velocity
                        selected_player.turn("right")
                    if event.key == pygame.K_LEFT:
                        selected_player.vel_x += -selected_player.velocity
                        selected_player.turn("left")
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        selected_player.vel_y += selected_player.velocity
                    if event.key == pygame.K_DOWN:
                        selected_player.vel_y += -selected_player.velocity
                    if event.key == pygame.K_RIGHT:
                        selected_player.vel_x += -selected_player.velocity
                    if event.key == pygame.K_LEFT:
                        selected_player.vel_x += selected_player.velocity

                # diagonal direction control
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    if keys[pygame.K_RIGHT]:
                        selected_player.turn("upright")
                    elif keys[pygame.K_LEFT]:
                        selected_player.turn("upleft")
                elif keys[pygame.K_DOWN]:
                    if keys[pygame.K_RIGHT]:
                        selected_player.turn("downright")
                    elif keys[pygame.K_LEFT]:
                        selected_player.turn("downleft")
                # stop player from moving when no keys are pressed
                else:
                    selected_player.vel_y = 0
                if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                    selected_player.vel_x = 0

            player1.update()
            player2.update()

            pygame.display.update()

            # send updates to server
            decoded_data[selected_data]["x"] = selected_player.x
            decoded_data[selected_data]["y"] = selected_player.y
            decoded_data[selected_data]["direction"] = selected_player.direction
            decoded_data[selected_data]["timestamp"] = pygame.time.get_ticks()

            package = pickle.dumps(decoded_data)
            client_socket.sendall(package)

        # Close the socket connection and Pygame
        client_socket.close()
        pygame.quit()
