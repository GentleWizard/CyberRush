import pygame

from .text import Text
from .ui import UiElement


class Slider(UiElement):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        game,
        text=None,
        font=None,
        text_color=(0, 0, 0),
        track_color=(255, 255, 255),
        slider_color=(100, 100, 100),
        slider_size=(25, 35),
        min_value=0,
        max_value=100,
        default_value=50,
        label=None,
        label_color=(255, 255, 255),
    ):
        super().__init__(x, y, width, height, game)
        self.slider_hovered = None
        self.text_color = text_color
        self.slider_color = slider_color
        self.font = font
        self.font_size = self.height // 2
        self.text = text
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.value = self.default_value
        self.slider_rect = None
        self.slider_width, self.slider_height = slider_size
        self.track_color = track_color
        self.label_text = label
        self.label_color = label_color

        self.track = pygame.Surface((self.width, self.height))
        self.track.fill(self.track_color)
        self.rect = self.track.get_rect(center=(self.x, self.y))

        self.slider = pygame.Surface((self.slider_width, self.slider_height))
        self.slider.fill(self.slider_color)
        self.slider_rect = self.slider.get_rect(center=self.rect.center)

        self.slider_rect.centerx = self.rect.x + (
            self.value / self.max_value * self.width
        )

        self.inner_text = Text(
            self.rect.centerx,
            self.rect.centery,
            self.rect.width,
            self.rect.height,
            self.game,
            text=self.text,
            font=self.font,
            font_size=self.font_size,
            text_color=self.text_color,
        )

        self.label = Text(
            self.rect.centerx,
            self.rect.bottom - self.rect.height * 1.5,
            self.rect.width,
            self.rect.height,
            self.game,
            text=self.label_text,
            font=self.font,
            font_size=self.font_size,
            text_color=self.label_color,
        )

        self.sliding = False

    def update(self, dt):
        if self.active:
            self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
            self.slider_hovered = self.slider_rect.collidepoint(pygame.mouse.get_pos())

            if self.slider_hovered and self.game.left_click_held:
                self.sliding = True
            elif self.sliding and not self.game.left_click_held:
                self.sliding = False

            if self.sliding:
                if pygame.mouse.get_pos()[0] <= self.rect.left:
                    self.slider_rect.left = self.rect.left
                elif pygame.mouse.get_pos()[0] >= self.rect.right:
                    self.slider_rect.right = self.rect.right
                else:
                    self.slider_rect.centerx = pygame.mouse.get_pos()[0]

                self.value = int(
                    (pygame.mouse.get_pos()[0] - self.rect.x)
                    / self.width
                    * self.max_value
                )
                self.value = max(self.min_value, min(self.max_value, self.value))

            if self.hover_event(global_change=True, hover_rect=self.slider_rect):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),
            if self.unhover_event(global_change=True, hover_rect=self.slider_rect):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),

            self.slider_rect.left = max(self.rect.left, self.slider_rect.left)
            self.slider_rect.right = min(self.rect.right, self.slider_rect.right)

    def draw(self, screen):
        screen.blit(self.track, self.rect)
        screen.blit(self.slider, self.slider_rect)
        self.inner_text.draw(screen)
        self.label.draw(screen)

    def set_active(self, active):
        self.active = active
        if not self.active:
            self.track.fill((100, 100, 100))
            self.slider.fill((50, 50, 50))
            self.inner_text.set_alpha(50)
            self.label.set_alpha(50)
        else:
            self.track.fill(self.track_color)
            self.slider.fill(self.slider_color)
            self.inner_text.set_alpha(255)
            self.label.set_alpha(255)

    def update_slider(
        self,
        x: int = None,
        y: int = None,
        width: int = None,
        height: int = None,
        track_color: tuple[int, int, int] = None,
        slider_color: tuple[int, int, int] = None,
        slider_size: tuple[int, int] = None,
        inner_text: str = None,
        label_text: str = None,
        label_color: tuple[int, int, int] = None,
    ):
        self.width = width if width else self.width
        self.height = height if height else self.height
        self.x = x if x else self.x
        self.y = y if y else self.y
        self.track_color = track_color if track_color else self.track_color
        self.slider_color = slider_color if slider_color else self.slider_color
        self.slider_width, self.slider_height = (
            slider_size if slider_size else (self.slider_width, self.slider_height)
        )
        self.inner_text.update_text(
            text=inner_text if inner_text else self.inner_text.text,
        )
        self.label.update_text(
            text=label_text if label_text else self.label.text,
            font_color=label_color if label_color else self.label.text_color,
        )

        self.track = pygame.Surface((self.width, self.height))
        self.track.fill(self.track_color)
        self.rect = self.track.get_rect(center=(self.x, self.y))

        self.slider = pygame.Surface((self.slider_width, self.slider_height))
        self.slider.fill(self.slider_color)
        self.slider_rect = self.slider.get_rect(center=self.rect.center)

        self.slider_rect.centerx = self.rect.x + (
            self.value / self.max_value * self.width
        )

        self.inner_text.rect.center = self.rect.center
        self.label.rect.centerx = self.rect.centerx
        self.label.rect.bottom = self.rect.bottom - self.rect.height * 1.5
