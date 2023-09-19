import pygame
from pygame.sprite import Sprite


class Button(Sprite):
    def __init__(
        self,
        x,
        y,
        function,
        width=100,
        height=50,
        colour=(255, 255, 255),
        font_colour=(0, 0, 0),
        text="Button",
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.font_colour = font_colour
        self.font = pygame.font.SysFont("Arial", 20)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = x

        self.alive = True

        self.text = self.font.render(self.text, True, self.font_colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.click_delay = 100
        self.last_click_time = 0

        self.function = function

    def update(self):
        if self.alive == False:
            return
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidelistall([pygame.Rect(mouse_pos, (1, 1))]):
            self.image.fill(
                (self.colour[0] - 40, self.colour[1] - 40, self.colour[2] - 40)
            )
            if pygame.mouse.get_pressed()[0]:
                if pygame.mouse.get_pressed()[0]:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_click_time > self.click_delay:
                        self.last_click_time = current_time
                        self.function()
        else:
            self.image.fill(self.colour)

    def blit(self, screen):
        if self.alive == False:
            return
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def set_text(self, text):
        self.text = text
        self.text = self.font.render(self.text, True, self.font_colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def set_colour(self, colour):
        self.colour = colour
        self.image.fill(self.colour)

    def set_font(self, font):
        self.font = font
        self.text = self.font.render(self.text, True, self.font_colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def set_font_colour(self, font_colour):
        self.font_colour = font_colour
        self.text = self.font.render(self.text, True, self.font_colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.text_rect.center = self.rect.center

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.text_rect.center = self.rect.center
