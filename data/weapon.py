import pygame


class Weapon:
    def __init__(self, user, target) -> None:
        pass


class Katana(Weapon):
    def __init__(self, user, target) -> None:
        super().__init__(user, target)
        self.dmg = 15
        self.images = []
