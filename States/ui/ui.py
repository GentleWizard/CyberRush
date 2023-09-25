import pygame
from pygame.sprite import Sprite


class UiElement(Sprite):
    def __init__(self, x, y, width, height, game):
        super().__init__()
        self.rect = None
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.hovered = False
        self.active = True

    def click_event(self, *function, rect: pygame.Rect):
        if self.active:
            if self.game.left_clicked and self.hover_event(
                global_change=True, hover_rect=rect
            ):
                for function in function:
                    function()
                return True
            else:
                return False

    def hover_event(self, hover_rect: pygame.Rect, global_change=False, forced=False):
        if self.active and not forced:
            mouse_collision = hover_rect.collidepoint(pygame.mouse.get_pos())
            self.__calculate_hovered(mouse_collision)
            if global_change:
                if mouse_collision and self.game.hovered == self:
                    return True
                else:
                    return False
            else:
                if mouse_collision:
                    return True
                else:
                    return False

    def unhover_event(self, hover_rect: pygame.Rect, global_change=False, forced=False):
        if self.active and not forced:
            mouse_collision = hover_rect.collidepoint(pygame.mouse.get_pos())
            self.__calculate_hovered(mouse_collision)
            if global_change:
                if self.game.hovered is None and not mouse_collision:
                    return True
                else:
                    return False
            else:
                if not mouse_collision:
                    return True
                else:
                    return False

    def __calculate_hovered(self, mouse_collision):
        if mouse_collision and self.game.hovered is None:
            self.game.hovered = self
        elif mouse_collision and self.game.hovered != self:
            self.game.hovered = self
        elif not mouse_collision and self.game.hovered == self:
            self.game.hovered = None
