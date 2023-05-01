import pygame
from data.game_manager import Game_manager
import socket
import sys

pygame.init()
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((1000, 800))
fps = 60


game_manager = Game_manager(screen, fps)
game_manager.state()
