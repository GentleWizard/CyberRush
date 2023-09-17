import pygame
from pygame.sprite import Sprite


class __UserInterface(Sprite):
    def __init__(self, x, y, text=True, image=False, image_path=None):
        super().__init__()
        if text:
            image = False
            self.font = pygame.font.SysFont("Arial", 20)
            self.colour = (255, 255, 255)
            self.content = "Hello World"
            self.text = self.font.render(self.content, True, self.colour)
        if image:
            text = False
            self.sprite = pygame.image.load(image_path)
        else:
            self.sprite = pygame.Surface((50, 60))
            self.sprite.fill((150, 255, 0))

        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

        self.rect.left = max(self.rect.left, 0)
        if self.rect.right >= self.game_width:
            self.rect.right = self.game_width
        self.rect.top = max(self.rect.top, 0)
        if self.rect.bottom >= self.game_height:
            self.rect.bottom = self.game_height

    def set_content(self, content):
        """Only works on text!"""
        self.content = content
        self.text = self.font.render(self.content, True, self.colour)

    def set_colour(self, colour):
        """Only works on text!"""
        self.colour = colour
        self.text = self.font.render(self.content, True, self.colour)

    def set_font(self, font):
        """Only works on text!"""
        self.font = font
        self.text = self.font.render(self.content, True, self.colour)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        if self.text:
            screen.blit(self.text, self.rect)
        if self.sprite:
            screen.blit(self.sprite, self.rect)


class player_Health_Bar(__UserInterface):
    def __init__(self, x, y, player, text=True, image=False, image_path=None):
        super().__init__(x, y, text, image, image_path)
        self.player = player
        self.content = f"{self.player.health}"
        self.text = self.font.render(self.content, True, self.colour)

        self.rect = self.text.get_rect()

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
            self.__calculate_health_colour()
        self.text = self.font.render(self.content, True, self.health_colour)

        if self.player.health <= 0:
            self.kill()

    def __calculate_health_colour(self):
        r = 255 * (1 - self.player.health_percentage) * 2
        g = 255 * self.player.health_percentage
        b = 0
        r = min(r, 255)
        g = min(g, 255)
        b = min(b, 255)
        self.health_colour = (r, g, b)


class player_Data_Cubes(__UserInterface):
    def __init__(self, x, y, player, text=True, image=False, image_path=None):
        super().__init__(x, y, text, image, image_path)
        self.player = player
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.text = self.font.render(self.content, True, self.colour)

    def update(self):
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.text = self.font.render(self.content, True, self.colour)
