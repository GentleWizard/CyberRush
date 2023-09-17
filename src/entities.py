import random

import pygame
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, image=False):
        super().__init__()
        # Stats
        self.health = 100
        self.max_health = 100
        self.health_percentage = self.health / self.max_health
        self.speed = 3
        self.alive = True

        # Data Cubes
        self.data_cubes = 0
        self.data_cubes_cooldown = 0
        self.data_cubes_cooldown_max = 20

        # Movement Animation
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

        self.health_percentage = self.health / 100

    def pickup_data_cube(self):
        if self.data_cubes_cooldown > 0:
            return
        self.data_cubes += 1
        self.data_cubes_cooldown = self.data_cubes_cooldown_max


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


class Enemy(Sprite):
    def __init__(self, x, y, image=False):
        super().__init__()
        if image:
            self.sprite = pygame.image.load("assets/enemy.png")
        else:
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((255, 0, 0))

        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hitdelay = 0
        self.damage = 10

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

    def update(self):
        if self.hitdelay > 0:
            self.hitdelay -= 1

    def attack(self, player):
        if self.hitdelay > 0:
            return
        player.health -= self.damage + player.data_cubes
        self.hitdelay = 65
