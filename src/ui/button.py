import pygame
from pygame.sprite import Sprite


class Button(Sprite):
    def __init__(
        self,
        x,
        y,
        function=lambda: print("Button pressed"),
        width=100,
        height=50,
        colour=(255, 255, 255),
        hover_colour=(200, 200, 200),
        font_hover_colour=(0, 0, 0),
        font_colour=(0, 0, 0),
        font="Arial",
        font_size=20,
        text="Button",
        bold=False,
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.colour = colour
        self.content = text
        self.font_colour = font_colour
        self.font = pygame.font.SysFont(font, font_size, bold)
        self.hover_colour = hover_colour
        self.font_hover_colour = font_hover_colour

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.text = self.font.render(self.content, True, self.font_colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.click_delay = 100
        self.last_click_time = 0

        self.function = function

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidelistall([pygame.Rect(mouse_pos, (1, 1))]):
            self.image.fill(self.hover_colour)
            self.text = self.font.render(self.content, True, self.font_hover_colour)
            if pygame.mouse.get_pressed()[0]:
                if pygame.mouse.get_pressed()[0]:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_click_time > self.click_delay:
                        self.last_click_time = current_time
                        self.function()
        else:
            self.image.fill(self.colour)
            self.text = self.font.render(self.content, True, self.font_colour)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def set_text(self, text):
        self.content = text
        self.text = self.font.render(self.content, True, self.font_colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def set_colour(self, colour):
        self.colour = colour
        self.image.fill(self.colour)

    def set_font(self, font):
        self.font = font
        self.text = self.font.render(self.content, True, self.font_colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def set_font_colour(self, font_colour):
        self.font_colour = font_colour
        self.text = self.font.render(self.content, True, self.font_colour)
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
