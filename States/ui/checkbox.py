import pygame

from .ui import UiElement

# TODO make the checkbox class work with the text class
class Checkbox(UiElement):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        game,
        text=None,
        text_color=(255, 255, 255),
        outer_box_color=(255, 255, 255),
        inner_box_color=(0, 0, 0),
        font=None,
    ):
        super().__init__(x, y, width, height, game)
        self.text_color = text_color
        self.font = font
        self.content = text

        self.outer_box_color = outer_box_color
        self.inner_box_color = inner_box_color

        self.outer_box = pygame.Surface((self.width, self.height))
        self.outer_box.fill(self.outer_box_color)
        self.rect = self.outer_box.get_rect(center=(self.x, self.y))

        self.inner_box = pygame.Surface((self.width // 1.3, self.height // 1.3))
        self.inner_box.fill(self.inner_box_color)
        self.inner_box_rect = self.inner_box.get_rect(center=self.rect.center)

        self.text = self.font.render(self.content, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.text_rect.bottom = self.rect.top - 10

        self.toggled = False

    def update(self, dt):
        if self.active:
            if self.hover_event(global_change=True, hover_rect=self.rect):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),
            if self.unhover_event(global_change=True, hover_rect=self.rect):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),

    def draw(self, screen):
        screen.blit(self.outer_box, self.rect)
        screen.blit(self.text, self.text_rect)
        if self.toggled:
            screen.blit(self.inner_box, self.inner_box_rect)

    def toggle(self, *functions):
        self.toggled = not self.toggled
        if self.toggled:
            for function in functions:
                function()
        else:
            for function in functions:
                function()

    def update_pos(self, x, y):
        self.rect = self.outer_box.get_rect(center=(x, y))
        self.inner_box_rect = self.inner_box.get_rect(center=self.rect.center)
        self.text_rect = self.text.get_rect(
            bottom=self.rect.top, centerx=self.rect.centerx
        )

    def update_text(self, text):
        self.content = text
        self.text = self.font.render(self.content, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update_text_color(self, color):
        self.text_color = color
        self.text = self.font.render(self.content, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update_outer_box_color(self, color):
        self.outer_box_color = color
        self.outer_box.fill(self.outer_box_color)

    def update_inner_box_color(self, color):
        self.inner_box_color = color
        self.inner_box.fill(self.inner_box_color)

    def update_font(self, font):
        self.font = font
        self.text = self.font.render(self.content, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update_size(self, width=None, height=None):
        self.width = width
        self.height = height
        self.outer_box = pygame.Surface((self.width, self.height))
        self.outer_box.fill(self.outer_box_color)
        self.rect = self.outer_box.get_rect(center=(self.x, self.y))
        self.inner_box = pygame.Surface((self.width // 1.3, self.height // 1.3))
        self.inner_box.fill(self.inner_box_color)
        self.inner_box_rect = self.inner_box.get_rect(center=self.rect.center)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def set_active(self, active):
        self.active = active

    def set_toggled(self, toggled):
        self.toggled = toggled
        if not self.toggled:
            self.outer_box.fill(self.outer_box_color)
            self.inner_box.fill(self.inner_box_color)
            self.text.set_alpha(255)
        else:
            self.outer_box.fill((100, 100, 100))
            self.inner_box.fill((50, 50, 50))
            self.text.set_alpha(50)
