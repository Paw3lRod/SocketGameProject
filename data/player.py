import pygame
import math
pygame.init()


class Player:
    def __init__(self, selected_image, x, y):
        self.image_file = selected_image
        self.image = pygame.image.load(
            "data/images/" + selected_image + ".png")
        self.image = pygame.transform.scale(self.image, (115, 115))
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
        self.hp = 200
        self.hit = False
        self.hittimer = 0

    def update(self):
        self.handle_hit()

        # turn accordingly
        if self.vel_x > 0:
            if self.vel_y < 0:
                self.turn("upright")
            elif self.vel_y > 0:
                self.turn("downright")
            else:
                self.turn("right")
        elif self.vel_x < 0:
            if self.vel_y < 0:
                self.turn("upleft")
            elif self.vel_y > 0:
                self.turn("downleft")
            else:
                self.turn("left")
        else:
            if self.vel_y < 0:
                self.turn("up")
            elif self.vel_y > 0:
                self.turn("down")

        self.x += self.vel_x
        self.y += self.vel_y

    def turn(self, direction):
        self.image = pygame.transform.scale(
            pygame.transform.rotate(pygame.image.load("data/images/" + self.image_file + ".png"), self.directions[direction]), self.scales[direction])

    def move(self, vel_x, vel_y, startstop):
        if startstop == "start":
            self.vel_x += (vel_x) * self.velocity
            self.vel_y += (vel_y) * self.velocity
        else:
            self.vel_x -= (vel_x) * self.velocity
            self.vel_y -= (vel_y) * self.velocity

        # adjust speed for diagonal movement
        if self.vel_x != 0 and self.vel_y != 0:
            if self.vel_x < 0:
                self.vel_x = -math.sqrt((self.velocity ** 2) / 2)
            else:
                self.vel_x = math.sqrt((self.velocity ** 2) / 2)
            if self.vel_y < 0:
                self.vel_y = -math.sqrt((self.velocity ** 2) / 2)
            else:
                self.vel_y = math.sqrt((self.velocity ** 2) / 2)

        # check if velocity is too high
        if self.vel_x > self.velocity:
            self.vel_x = self.velocity
        elif self.vel_x < -self.velocity:
            self.vel_x = self.velocity
        if self.vel_y > self.velocity:
            self.vel_y = self.velocity
        elif self.vel_y < -self.velocity:
            self.vel_y = self.velocity

    def change_velocity(self, new_velocity):
        self.velocity = new_velocity
        self.positionchanges = {"down": [0, self.velocity], "up": [0, -self.velocity], "right": [
            self.velocity, 0], "left": [-self.velocity, 0], "upright": [self.velocity, -self.velocity], "upleft": [-self.velocity, -self.velocity], "downright": [self.velocity, self.velocity], "downleft": [-self.velocity, self.velocity]}

    def get_hit(self, dmg):
        if not self.hit:
            self.image = pygame.image.load(
                "data/images/hit.png")
            self.image = pygame.transform.scale(self.image, (115, 115))
            self.hit = True
            self.hp -= dmg

    def handle_hit(self):
        if self.hit:
            self.hittimer += 1
            if self.hittimer >= 150:
                self.image = pygame.image.load(
                    "data/images/" + self.image_file + ".png")
                self.image = pygame.transform.scale(self.image, (115, 115))
                self.hittimer = 0
                self.hit = False
