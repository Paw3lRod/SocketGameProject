import pygame


class Button:
    def __init__(self, width, height, text, textsize, bgcolor, pos) -> None:
        self.bgcolor = bgcolor
        self.pos = pos
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("arial", textsize)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.textpos = (self.pos[0] + (width) / 2 - (self.text.get_width()) / 2,
                        self.pos[1] + (height) / 2 - (self.text.get_height()) / 2)
        self.rect = pygame.Rect(pos, (width, height))
        self.selected = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgcolor, self.rect)
        screen.blit(self.text, self.textpos)

        if self.selected:
            pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect(
                self.pos[0], self.pos[1], self.width, self.height), 3)

    def set_pos(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(pos, (self.width, self.height))
        self.textpos = (self.pos[0] + (self.width) / 2 - (self.text.get_width()) / 2,
                        self.pos[1] + (self.height) / 2 - (self.text.get_height()) / 2)

    def select(self, state):
        self.selected = state


def draw_button_list(button_list, counter, screen, space, pos):
    for i in range(len(button_list)):
        button_list[i].set_pos((pos[0] + (i * space), pos[1]))
        if i == counter.index:
            button_list[i].select(True)
        else:
            button_list[i].select(False)

        button_list[i].draw(screen)
