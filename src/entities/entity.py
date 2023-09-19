import pygame
from pygame.sprite import Sprite


class Entity(Sprite):
    def __init__(self, x, y, colour=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
