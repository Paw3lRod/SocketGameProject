import pygame


class Weapon:
    def __init__(self, user, target) -> None:
        self.user = user
        self.target = target

        self.images = []
        self.image_index = 0

    def load_images(self, path, sprite_width, sprite_height, width, height):
        sprite_sheet_path = path

        sprite_sheet = pygame.image.load(sprite_sheet_path)
        sprite_sheet = sprite_sheet.convert_alpha()

        images = []

        # Assuming all sprites are on the same row
        for sprite_index in range(sprite_sheet.get_width() // sprite_width):
            x = sprite_index * sprite_width
            y = 0  # Since all sprites are on the same row

            # Extract the sprite from the sprite sheet
            sprite = sprite_sheet.subsurface(
                pygame.Rect(x, y, sprite_width, sprite_height)
            )

            resized_sprite = pygame.transform.scale(sprite, (width, height))

            images.append(resized_sprite)

        return images

    def display(self, screen):
        if self.user.direction == "down":
            screen.blit(
                self.images[self.image_index],
                (self.user.x - 20, self.user.y + 80),
            )

        elif self.user.direction == "up":
            image = pygame.transform.rotate(self.images[self.image_index], 180)
            screen.blit(image, (self.user.x - 3, self.user.y - 80))

        elif self.user.direction == "left":
            image = pygame.transform.rotate(self.images[self.image_index], 270)
            screen.blit(image, (self.user.x - 80, self.user.y - 20))

        elif self.user.direction == "right":
            image = pygame.transform.rotate(self.images[self.image_index], 90)
            screen.blit(image, (self.user.x + 84, self.user.y - 4))

        elif self.user.direction == "upright":
            image = pygame.transform.rotate(self.images[self.image_index], 135)
            screen.blit(image, (self.user.x + 54, self.user.y - 60))

        elif self.user.direction == "upleft":
            image = pygame.transform.rotate(self.images[self.image_index], -135)
            screen.blit(image, (self.user.x - 64, self.user.y - 76))

        elif self.user.direction == "downright":
            image = pygame.transform.rotate(self.images[self.image_index], 45)
            screen.blit(image, (self.user.x + 40, self.user.y + 50))

        elif self.user.direction == "downleft":
            image = pygame.transform.rotate(self.images[self.image_index], -45)
            screen.blit(image, (self.user.x - 80, self.user.y + 40))


class Katana(Weapon):
    def __init__(self, user, target) -> None:
        super().__init__(user, target)
        self.dmg = 15
        self.images = self.load_images(
            "data/images/weapons/katana/katana_sh.png", 72, 57, 144, 114
        )

        # basic attack
        self.attack = False
        self.slice_timer = 0

    def slice(self):
        self.slice_timer += 1

        if self.slice_timer >= 10:
            self.image_index += 1
            self.slice_timer = 0

            if self.image_index >= len(self.images):
                self.image_index = 0
                self.attack = False

        # detect if enemy hit
        if (
            self.images[self.image_index]
            .get_rect()
            .colliderect(self.target.image.get_rect())
        ):
            self.target.get_hit(self.dmg)

    def display(self, screen):
        if self.attack:
            self.slice()

        return super().display(screen)
