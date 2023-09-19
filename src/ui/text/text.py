import pygame
from pygame.sprite import Sprite


class Text(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 20)
        self.colour = (255, 255, 255)
        self.content = "Hello World"
        self.image = self.font.render(self.content, True, self.colour)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.alive = True

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.game_width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, self.game_height)

    def set_content(self, content):
        self.content = content
        self.image = self.font.render(self.content, True, self.colour)

    def set_colour(self, colour):
        self.colour = colour
        self.image = self.font.render(self.content, True, self.colour)

    def set_font(self, font):
        self.font = font
        self.image = self.font.render(self.content, True, self.colour)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        if self.alive == False:
            return
        screen.blit(self.image, self.rect)
