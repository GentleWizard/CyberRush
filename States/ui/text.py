from os import PathLike
from typing import Literal, Sequence, IO

import pygame
from pygame import Color

from States.ui.ui import UiElement


class FontTypeHinting:
    size: int
    name: str | bytes | PathLike[str | bytes] | IO[bytes | str] | None


class RenderTypeHinting:
    text: str | bytes | None
    antialias: Literal[True, False] | bool
    color: Color | int | str | tuple[int, int, int, int] | tuple[
        int, int, int
    ] | Sequence[int] | None
    Background: Color | int | str | tuple[int, int, int, int] | tuple[
        int, int, int
    ] | Sequence[int] | None = None


class Text(UiElement):
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
        font_size=None,
    ):
        super().__init__(x, y, width, height, game)
        self.x = x
        self.y = y
        self.font = font if font else self.game.font
        self.font_size = font_size if font_size else self.height // 2
        self.text = text
        self.text_color = text_color
        self.font_obj = pygame.font.Font(self.font, self.font_size)
        self.image = self.font_obj.render(self.text, True, self.text_color)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = width
        self.rect.height = height

    def update(self, dt):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        return self.image, self.rect

    def update_font(self, **kwargs: FontTypeHinting):
        self.font_obj = pygame.font.Font(
            kwargs["name"] if "name" in kwargs else self.font,
            kwargs["size"] if "size" in kwargs else self.font_size,
        )
        self.image = self.font_obj.render(self.text, True, self.text_color)
        return self.image

    def update_text(
        self, x=None, y=None, width=None, height=None, **kwargs: RenderTypeHinting
    ):
        self.image = self.font_obj.render(
            kwargs["text"] if "text" in kwargs else self.text,
            kwargs["antialias"] if "antialias" in kwargs else True,
            kwargs["color"] if "color" in kwargs else self.text_color,
            kwargs["background"] if "background" in kwargs else None,
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = x if x else self.rect.centerx
        self.rect.centery = y if y else self.rect.centery
        self.rect.width = self.width if width else self.rect.width
        self.rect.height = self.height if height else self.rect.height
        return self.rect

    def set_alpha(self, alpha: int):
        self.image.set_alpha(alpha)
        return self.image
