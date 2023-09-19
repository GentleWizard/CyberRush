import pygame

from .entity import Entity


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
