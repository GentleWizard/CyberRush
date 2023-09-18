import pygame
from pygame.sprite import Sprite


def calculate_health_colour(health_percentage, max_health):
    r = 255 * (1 - health_percentage) * 2
    g = 255 * health_percentage
    b = 0
    r = min(r, 255)
    g = min(g, 255)
    b = min(b, 255)
    return r, g, b


class __Text(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 20)
        self.colour = (255, 255, 255)
        self.content = "Hello World"
        self.text = self.font.render(self.content, True, self.colour)

        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.game_width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, self.game_height)

    def set_content(self, content):
        self.content = content
        self.text = self.font.render(self.content, True, self.colour)

    def set_colour(self, colour):
        self.colour = colour
        self.text = self.font.render(self.content, True, self.colour)

    def set_font(self, font):
        self.font = font
        self.text = self.font.render(self.content, True, self.colour)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.text, self.rect)


class player_Health_Bar(__Text):
    def __init__(self, x, y, player):
        super().__init__(x, y)
        self.player = player
        self.content = f"{self.player.health}"
        self.text = self.font.render(self.content, True, self.colour)

        self.rect = self.text.get_rect()
        self.health_percentage = self.player.health / self.player.max_health

        self.width = self.rect.width
        self.height = self.rect.height
        self.health_colour = (0, 255, 0)

    def update(self):
        self.content = f"{self.player.health}"

        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.x = self.player.rect.center[0] - (self.width // 1.5)
        self.rect.y = self.player.rect.center[1] - (self.height * 1.6)

        if self.player.health < self.player.max_health:
            self.health_percentage = self.player.health / self.player.max_health
            self.health_colour = calculate_health_colour(
                self.health_percentage, self.player.max_health
            )
        self.text = self.font.render(self.content, True, self.health_colour)


class player_Data_Cubes(__Text):
    def __init__(self, x, y, player):
        super().__init__(x, y)
        self.player = player
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.text = self.font.render(self.content, True, self.colour)

    def update(self):
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.text = self.font.render(self.content, True, self.colour)
