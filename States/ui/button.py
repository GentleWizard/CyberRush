import pygame

from .text import Text
from .ui import UiElement


class Button(UiElement):
    def __init__(
            self,
            game,
            x=None,
            y=None,
            width=None,
            height=None,
            text=None,
            font=None,
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font_size=None,
    ):
        super().__init__(x, y, width, height, game)
        self.x = x if x else self.game.width // 2
        self.y = y if y else self.game.height // 2
        self.width = width if width else self.game.width // 2
        self.height = height if height else self.game.height // 10
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = font
        self.font_size = font_size if font_size else self.height // 2
        self.content = text
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.text = Text(
            self.rect.centerx,
            self.rect.centery,
            self.rect.width,
            self.rect.height,
            self.game,
            text=self.content,
            font=self.font,
            font_size=self.font_size,
            text_color=self.text_color,
        )

        self.hover_color = (
            self.bg_color[0] - 50 if self.bg_color[0] - 50 >= 50 else 0,
            self.bg_color[1] - 50 if self.bg_color[1] - 50 >= 50 else 0,
            self.bg_color[2] - 50 if self.bg_color[2] - 50 >= 50 else 0,
        )
        self.unhover_color = self.bg_color

        self.active = True

    def update(self, dt):
        if self.active:
            if self.hover_event(self.rect):
                self.update_button(bg_color=self.hover_color)
            if self.unhover_event(self.rect):
                self.update_button(bg_color=self.unhover_color)
            if self.hover_event(global_change=True, hover_rect=self.rect):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.unhover_event(global_change=True, hover_rect=self.rect):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.text.update_font(size=self.height // 2)
        self.text.update(dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.text.draw(screen)

    def update_button(
            self,
            x: int = None,
            y: int = None,
            width: int = None,
            height: int = None,
            bg_color: tuple[int, int, int] = None,
            text: str = None,
            font: str = None,
            font_color: tuple[int, int, int] = None,
            font_size: int = None,
    ) -> None:
        self.width = width if width else self.width
        self.height = height if height else self.height
        self.x = x if x else self.x
        self.y = y if y else self.y
        self.bg_color = bg_color if bg_color else self.bg_color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text.update_text(
            font=font if font else self.font,
            font_color=font_color if font_color else self.text_color,
            font_size=font_size if font_size else self.font_size,
            text=text if text else self.content,
        )
        self.text.rect.centerx = self.rect.centerx
        self.text.rect.centery = self.rect.centery


    def set_active(self, active):
        self.active = active
        if not self.active:
            self.update_button(bg_color=(100, 100, 100))
            self.image.set_alpha(150)
            self.text.set_alpha(150)
        else:
            self.update_button(bg_color=self.bg_color)
            self.image.set_alpha(255)
            self.text.set_alpha(255)


# TODO: Make the load button that displays the save files data
class LoadButton(Button):
    pass
