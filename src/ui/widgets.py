import pygame
from pygame.sprite import Sprite


class Slider(Sprite):
    def __init__(
        self,
        x,
        y,
        width=100,
        height=20,
        colour=(255, 255, 255),
        hover_colour=(200, 200, 200),
        handle_colour=(0, 0, 0),
        handle_size=10,
        handle_hover_colour=(100, 100, 100),
        border_radius=10,
        label="",
        label_font="Arial",
        label_size=20,
        label_bold=False,
        label_colour=(0, 0, 0),
        text="",
        text_font="Arial",
        text_size=20,
        text_bold=False,
        text_colour=(0, 0, 0),
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.colour = colour

        self.hover_colour = hover_colour
        self.handle_colour = handle_colour
        self.handle_radius = handle_size
        self.handle_hover_colour = handle_hover_colour
        self.border_radius = border_radius

        self.label = label
        self.label_font_set = label_font
        self.label_font_size = label_size
        self.label_font_bold = label_bold
        self.label_font_colour = label_colour
        self.label_font = pygame.font.SysFont(
            self.label_font_set, self.label_font_size, self.label_font_bold
        )
        self.font_surface = self.label_font.render(
            self.label, True, self.label_font_colour
        )

        self.text = text
        self.text_font_set = text_font
        self.text_font_size = text_size
        self.text_font_bold = text_bold
        self.text_font_colour = text_colour
        self.text_font = pygame.font.SysFont(
            self.text_font_set, self.text_font_size, self.text_font_bold
        )
        self.text_surface = self.text_font.render(
            self.text, True, self.text_font_colour
        )

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        if self.width < self.height:
            self.handle_pos = self.rect.centery
        else:
            self.handle_pos = self.rect.centerx
        self.dragging = False

        self.handle_width = self.handle_radius * 2
        self.handle_height = self.handle_radius * 2

        self.handle_rect = pygame.Rect(
            self.rect.centerx - self.handle_radius,
            self.rect.centery - self.handle_radius,
            self.handle_width,
            self.handle_height,
        )

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image.fill(self.hover_colour)
            if pygame.mouse.get_pressed()[0]:
                self.dragging = True
        else:
            self.image.fill(self.colour)

        if self.dragging:
            self.handle_pos = mouse_pos[1] if self.width < self.height else mouse_pos[0]
            if pygame.mouse.get_pressed()[0] == 0:
                self.dragging = False

        # Clamp the handle position within the slider
        self.__clamp()

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Draw the track of the slider with rounded corners
        if self.width < self.height:
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen,
                    self.hover_colour,
                    pygame.Rect(
                        self.rect.left,
                        self.rect.top + self.border_radius,
                        self.width,
                        self.height - 2 * self.border_radius,
                    ),
                    border_radius=self.border_radius,
                )
            else:
                pygame.draw.rect(
                    screen,
                    self.colour,
                    pygame.Rect(
                        self.rect.left,
                        self.rect.top + self.border_radius,
                        self.width,
                        self.height - 2 * self.border_radius,
                    ),
                    border_radius=self.border_radius,
                )
        else:
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen,
                    self.hover_colour,
                    pygame.Rect(
                        self.rect.left + self.border_radius,
                        self.rect.top,
                        self.width - 2 * self.border_radius,
                        self.height,
                    ),
                    border_radius=self.border_radius,
                )
            else:
                pygame.draw.rect(
                    screen,
                    self.colour,
                    pygame.Rect(
                        self.rect.left + self.border_radius,
                        self.rect.top,
                        self.width - 2 * self.border_radius,
                        self.height,
                    ),
                    border_radius=self.border_radius,
                )

        if self.width < self.height:
            self.handle_rect = pygame.Rect(
                self.rect.centerx - self.handle_radius,
                self.handle_pos - self.handle_radius,
                self.handle_radius * 2,
                self.handle_radius * 2,
            )
        else:
            self.handle_rect = pygame.Rect(
                self.handle_pos - self.handle_radius,
                self.rect.centery - self.handle_radius,
                self.handle_radius * 2,
                self.handle_radius * 2,
            )

        if self.width > self.height:
            label_surface = self.label_font.render(
                self.label, True, self.label_font_colour
            )
            label_rect = label_surface.get_rect()
            label_rect.centerx = self.rect.centerx
            label_rect.bottom = self.rect.top - self.label_font_size
        else:
            label_surface = self.label_font.render(
                self.label, True, self.label_font_colour
            )
            label_rect = label_surface.get_rect()
            label_rect.centerx = self.rect.centerx
            label_rect.top = self.rect.top - self.label_font_size

        screen.blit(label_surface, label_rect)

        text_surface = self.text_font.render(self.text, True, self.text_font_colour)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.rect.centerx
        text_rect.centery = self.rect.centery

        screen.blit(text_surface, text_rect)

        # Draw the handle of the slider
        if self.width < self.height:
            if self.handle_rect.collidepoint(mouse_pos):
                pygame.draw.circle(
                    screen,
                    self.handle_hover_colour,
                    (self.rect.centerx, self.handle_pos),
                    self.handle_radius,
                )
            else:
                pygame.draw.circle(
                    screen,
                    self.handle_colour,
                    (self.rect.centerx, self.handle_pos),
                    self.handle_radius,
                )
        else:
            if self.handle_rect.collidepoint(mouse_pos):
                pygame.draw.circle(
                    screen,
                    self.handle_hover_colour,
                    (self.handle_pos, self.rect.centery),
                    self.handle_radius,
                )
            else:
                pygame.draw.circle(
                    screen,
                    self.handle_colour,
                    (self.handle_pos, self.rect.centery),
                    self.handle_radius,
                )

    def get_value(self, invert=False):
        if self.width < self.height:
            slider_length = self.height - 2 * (self.border_radius + self.handle_radius)
            handle_pos = (
                self.handle_pos
                - self.rect.top
                - self.border_radius
                - self.handle_radius
            )
        else:
            slider_length = self.width - 2 * (self.border_radius + self.handle_radius)
            handle_pos = (
                self.handle_pos
                - self.rect.left
                - self.border_radius
                - self.handle_radius
            )

        value = handle_pos / slider_length

        if invert:
            value = 1 - value

        return int(value * 100)

    def __clamp(self):
        if self.width < self.height:
            min_handle_pos = self.rect.top + self.handle_radius + self.border_radius
            max_handle_pos = self.rect.bottom - self.handle_radius - self.border_radius
        else:
            min_handle_pos = self.rect.left + self.handle_radius + self.border_radius
            max_handle_pos = self.rect.right - self.handle_radius - self.border_radius

        self.handle_pos = max(min_handle_pos, min(self.handle_pos, max_handle_pos))

    def set_text(self, text):
        self.text = text
        self.text_surface = self.text_font.render(
            self.text, True, self.text_font_colour
        )


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
