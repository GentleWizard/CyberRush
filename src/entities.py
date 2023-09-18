import random
from math import sqrt

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
        self.acceleration = self.speed / 7
        self.deceleration = self.speed / 10
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

        self.dx = 0
        self.dy = 0

        # Rect
        self.rect = self.sprite.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

    def movement(self):
        if len(self.direction) > 0:
            if self.dx != 0 and self.dy != 0:
                self.dx /= sqrt(2)
                self.dy /= sqrt(2)
            if pygame.K_w in self.direction and self.dy > -self.speed:
                self.dy -= self.acceleration
            if pygame.K_s in self.direction and self.dy < self.speed:
                self.dy += self.acceleration
            if pygame.K_a in self.direction and self.dx > -self.speed:
                self.dx -= self.acceleration
            if pygame.K_d in self.direction and self.dx < self.speed:
                self.dx += self.acceleration

        self.dy = min(self.dy, self.speed)
        self.dy = max(self.dy, -self.speed)
        self.dx = min(self.dx, self.speed)
        self.dx = max(self.dx, -self.speed)

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.dx > 0 and pygame.K_d not in self.direction:
            self.dx -= self.deceleration
            self.dx = max(self.dx, 0)
        if self.dx < 0 and pygame.K_a not in self.direction:
            self.dx += self.deceleration
            self.dx = min(self.dx, 0)
        if self.dy > 0 and pygame.K_s not in self.direction:
            self.dy -= self.deceleration
            self.dy = max(self.dy, 0)
        if self.dy < 0 and pygame.K_w not in self.direction:
            self.dy += self.deceleration
            self.dy = min(self.dy, 0)

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.game_width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, self.game_height)

        # print(f"a: {self.acceleration} d: {self.deceleration}")
        print(f"dx: {self.dx} dy: {self.dy}")
        # print(f"x: {self.rect.x} y: {self.rect.y}")
        # print(f"k: {self.direction}")

    def reset_speed(self):
        self.acceleration = 0
        self.deceleration = 0
        self.dx = 0
        self.dy = 0

    def update(self):
        if self.data_cubes_cooldown > 0:
            self.data_cubes_cooldown -= 1
        self.movement()

        self.health_percentage = self.health / 100

        self.health = min(self.health, self.max_health)

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

        self.game_width = game_width - self.rect.width
        self.game_height = game_height - self.rect.height

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

    def randomise_position(self):
        if self.rect.x <= 0:
            self.rect.x = random.randint(0, self.game_width + 15)
        if self.rect.y <= 0:
            self.rect.y = random.randint(0, self.game_height + 15)
        if self.rect.x >= self.game_width:
            self.rect.x = random.randint(0, self.game_width - 15)
        if self.rect.y >= self.game_height:
            self.rect.y = random.randint(0, self.game_height - 15)

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.game_width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, self.game_height)


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
        self.speed = 3

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

    def update(self):
        if self.hitdelay > 0:
            self.hitdelay -= 1

        self.ai()

    def attack(self, player):
        if self.hitdelay > 0:
            return
        player.health -= self.damage + player.data_cubes
        self.hitdelay = 65

    def ai(self):
        pass
