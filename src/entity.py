import random

import pygame
from pygame.sprite import Sprite


class Entity(Sprite):
    def __init__(self, x, y, colour=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.display_info = pygame.display.Info()
        self.game_width = self.display_info.current_w
        self.game_height = self.display_info.current_h

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, x, y, colour=(0, 0, 255)):
        super().__init__(x, y, colour)
        # Stats
        self.health = 100
        self.max_health = 100
        self.health_percentage = self.health / self.max_health
        self.speed = 3
        self.acceleration = self.speed / 7
        self.deceleration = self.speed / 10

        # Data Cubes
        self.data_cubes = 0
        self.data_cubes_cooldown = 0
        self.data_cubes_cooldown_max = 20

        # Movement Animation
        self.direction = []

        self.dx = 0
        self.dy = 0

    def movement(self):
        if len(self.direction) > 0:
            if self.dx != 0 and self.dy != 0:
                self.dx /= 1.35
                self.dy /= 1.35
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

    def reset_speed(self):
        self.acceleration = 0
        self.deceleration = 0
        self.dx = 0
        self.dy = 0

    def update(self):
        if self.health <= 0:
            self.kill()

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


class Enemy(Entity):
    def __init__(self, x, y, colour=(255, 0, 0)):
        super().__init__(x, y, colour)

        self.hitdelay = 0
        self.damage = 10
        self.speed = 3

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


class DataCube(Entity):
    def __init__(self, colour=(0, 255, 0), x=0, y=0):
        super().__init__(x, y, colour)

    def randomise_position(self):
        self.rect.x = random.randint(50, self.game_width - 50)
        self.rect.y = random.randint(50, self.game_height - 50)
