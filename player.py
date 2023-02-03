import pygame


class Player:
    def __init__(self):
        self.image = pygame.image.load("images/jeremy.png")
        self.image = pygame.transform.scale(self.image, (115, 115))
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.velocity = 5
        self.directions = {"down": 0, "up": 180,
                           "right": 90, "left": -90, "upright": 135, "upleft": -135, "downright": 45, "downleft": -45}
        self.scales = {"down": (115, 115), "up": (
            115, 115), "right": (115, 115), "left": (115, 115), "upright": (155, 155), "upleft": (155, 155), "downright": (155, 155), "downleft": (155, 155)}
        self.positionchanges = {"down": [0, self.velocity], "up": [0, -self.velocity], "right": [
            self.velocity, 0], "left": [-self.velocity, 0], "upright": [self.velocity, -self.velocity], "upleft": [-self.velocity, -self.velocity], "downright": [self.velocity, self.velocity], "downleft": [-self.velocity, self.velocity]}

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def turn(self, direction):
        self.vel_x = self.positionchanges[direction][0]
        self.vel_y = self.positionchanges[direction][1]
        self.image = pygame.transform.scale(
            pygame.transform.rotate(pygame.image.load("images/jeremy.png"), self.directions[direction]), self.scales[direction])
