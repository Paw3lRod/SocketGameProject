import pygame
import socket
from button import Button, draw_button_list
from counter import Counter

pygame.init()
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((1000, 800))


class Game_manager:
    def __init__(self) -> None:
        pass

    def intro_menu(self, screen):
        button_play = Button(200, 60, "Play online", 26,
                             (255, 112, 150), (0, 0))
        button_customize = Button(
            200, 60, "Customize", 26, (255, 112, 150), (0, 0))
        button_practice = Button(
            200, 60, "Practice", 26, (255, 112, 150), (0, 0))
        buttons = [button_customize, button_play, button_practice]
        selected_button = Counter(len(buttons), 0)

        while True:
            # blit
            screen.fill((255, 255, 255))
            draw_button_list(buttons, selected_button, screen,
                             space=250, pos=(150, 500))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    selected_button.dec()
                if keys[pygame.K_RIGHT]:
                    selected_button.inc()

            pygame.display.update()


game_manager = Game_manager()
game_manager.intro_menu(screen)
