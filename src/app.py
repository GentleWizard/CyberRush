import random
import sys

import pygame
from pygame.sprite import Sprite


class CyberRush:
    def __init__(self, width, height, title):
        # Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        self.width = width
        self.height = height

        # Entities
        self.player = Player(100, 100)
        self.data_cube = DataCube(width, height)

        # UI
        self.player_health_bar = player_Health_Bar(0, 0, self.player)
        self.player_data_cubes = player_Data_Cubes(0, 20, self.player)

        # Groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.data_cube_group = pygame.sprite.Group(self.data_cube)
        self.ui_group = pygame.sprite.Group(
            self.player_health_bar, self.player_data_cubes
        )

        # Keybinds
        self.movement_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
        self.ability_keys = [pygame.K_e, pygame.K_q]

    def handle_events(self):
        if pygame.sprite.groupcollide(
            self.player_group, self.data_cube_group, False, True
        ):
            self.player.pickup_data_cube()
            self.data_cube = DataCube(self.width, self.height)
            self.data_cube_group.add(self.data_cube)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in self.movement_keys:
                    current_direction = {"key": event.key}
                    self.player.direction.append(current_direction)

            if event.type == pygame.KEYUP:
                if event.key in self.movement_keys:
                    for direction in self.player.direction:
                        if event.key == direction.get("key"):
                            self.player.direction.remove(direction)

    def update(self):
        self.player_group.update()
        self.data_cube_group.update()
        self.ui_group.update()

    def draw(self):
        self.screen.fill((0, 0, 10))  # Keep at top of draw method

        # entities
        self.screen.blit(self.data_cube.sprite, self.data_cube.rect)
        self.screen.blit(self.player.sprite, self.player.rect)

        # UI
        self.screen.blit(self.player_health_bar.text, self.player_health_bar.rect)
        self.screen.blit(self.player_data_cubes.text, self.player_data_cubes.rect)

        pygame.display.flip()  # Keep at bottom of draw method

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

        sys.exit()


class Player(Sprite):
    def __init__(self, x, y, image=False):
        super().__init__()
        # Stats
        self.health = 100
        self.speed = 3

        # Data Cubes
        self.data_cubes = 0
        self.data_cubes_cooldown = 0
        self.data_cubes_cooldown_max = 20

        # Movement
        self.direction = []
        if image:
            self.walking_up_sprites = []
            self.walking_down_sprites = []
            self.walking_left_sprites = []
            self.walking_right_sprites = []
            standing_image = "assets/player/standing.png"
            self.sprite = pygame.image.load(standing_image)
        else:
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((255, 255, 255))

        # Rect
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

    def movement(self):
        if len(self.direction) == 0:
            return
        elif self.direction[-1].get("key") == pygame.K_w:
            self.rect.y -= self.speed
        elif self.direction[-1].get("key") == pygame.K_s:
            self.rect.y += self.speed
        elif self.direction[-1].get("key") == pygame.K_a:
            self.rect.x -= self.speed
        elif self.direction[-1].get("key") == pygame.K_d:
            self.rect.x += self.speed

        self.rect.left = max(self.rect.left, 0)
        if self.rect.right >= self.game_width:
            self.rect.right = self.game_width
        self.rect.top = max(self.rect.top, 0)
        if self.rect.bottom >= self.game_height:
            self.rect.bottom = self.game_height

    def update(self):
        if self.data_cubes_cooldown > 0:
            self.data_cubes_cooldown -= 1
        self.movement()

    def pickup_data_cube(self):
        if self.data_cubes_cooldown > 0:
            return
        self.data_cubes += 1
        self.data_cubes_cooldown = self.data_cubes_cooldown_max


class UserInterface(Sprite):
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


class player_Health_Bar(UserInterface):
    def __init__(self, x, y, player, text=True, image=False, image_path=None):
        super().__init__(x, y, text, image, image_path)
        self.player = player
        self.content = f"Health: {self.player.health}"
        self.text = self.font.render(self.content, True, self.colour)

    def update(self):
        self.content = f"Health: {self.player.health}"
        self.text = self.font.render(self.content, True, self.colour)


class player_Data_Cubes(UserInterface):
    def __init__(self, x, y, player, text=True, image=False, image_path=None):
        super().__init__(x, y, text, image, image_path)
        self.player = player
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.text = self.font.render(self.content, True, self.colour)

    def update(self):
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.text = self.font.render(self.content, True, self.colour)


class DataCube(Sprite):
    def __init__(self, game_width, game_height, image=False):
        super().__init__()
        if image:
            self.sprite = pygame.image.load("assets/data_cube.png")
        else:
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((0, 0, 150))

        self.rect = self.sprite.get_rect()

        self.game_width = game_width - self.rect.width - 15
        self.game_height = game_height - self.rect.height - 15

        self.rect.x = random.randint(0, self.game_width)
        self.rect.y = random.randint(0, self.game_height)

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

        self.rect.left = max(self.rect.left, 0)
        if self.rect.right >= self.game_width:
            self.rect.right = self.game_width
        self.rect.top = max(self.rect.top, 0)
        if self.rect.bottom >= self.game_height:
            self.rect.bottom = self.game_height


if __name__ == "__main__":
    game = CyberRush(800, 600, "CyberRush")
    game.run()
