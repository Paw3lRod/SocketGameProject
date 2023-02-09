import pygame
import math


class Player:
    def __init__(self, selected_image, x, y):
        self.image_file = pygame.image.load(
            "images/" + selected_image + ".png")
        self.image = pygame.transform.scale(self.image_file, (115, 115))
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.velocity = 2
        self.directions = {"down": 0, "up": 180,
                           "right": 90, "left": -90, "upright": 135, "upleft": -135, "downright": 45, "downleft": -45}
        self.scales = {"down": (115, 115), "up": (
            115, 115), "right": (115, 115), "left": (115, 115), "upright": (155, 155), "upleft": (155, 155), "downright": (155, 155), "downleft": (155, 155)}
        self.positionchanges = {"down": [0, self.velocity], "up": [0, -self.velocity], "right": [
            self.velocity, 0], "left": [-self.velocity, 0], "upright": [self.velocity, -self.velocity], "upleft": [-self.velocity, -self.velocity], "downright": [self.velocity, self.velocity], "downleft": [-self.velocity, self.velocity]}

    def update(self):
        # check if velocity is too high
        if self.vel_x > self.velocity:
            self.vel_x = self.velocity
        elif self.vel_x < -self.velocity:
            self.vel_x = self.velocity
        if self.vel_y > self.velocity:
            self.vel_y = self.velocity
        elif self.vel_y < -self.velocity:
            self.vel_y = self.velocity

        # check if player is heading diagonal
        if self.vel_x != 0 and self.vel_y != 0:
            if self.vel_x < 0:
                self.vel_x = -math.sqrt((self.velocity ** 2) / 2)
            else:
                self.vel_x = math.sqrt((self.velocity ** 2) / 2)
            if self.vel_y < 0:
                self.vel_y = -math.sqrt((self.velocity ** 2) / 2)
            else:
                self.vel_y = math.sqrt((self.velocity ** 2) / 2)

        self.x += self.vel_x
        self.y += self.vel_y

    def turn(self, direction):
        self.vel_x = self.positionchanges[direction][0]
        self.vel_y = self.positionchanges[direction][1]
        self.image = pygame.transform.scale(
            pygame.transform.rotate(pygame.image.load("images/jeremy.png"), self.directions[direction]), self.scales[direction])
