import math

import pygame

from .entity import Entity


class Player(Entity):
    def __init__(self, game, x, y, width, height, save_data):
        super().__init__(game, x, y, width, height)
        self.save_data = save_data
        self.game = game
        self.width = self.save_data["width"] if self.save_data else width
        self.height = self.save_data["height"] if self.save_data else height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.rect.center = (save_data["x"], save_data["y"]) if save_data else (x, y)

        multiplier = 10
        self.keys_pressed = pygame.key.get_pressed()
        self.velocity = [0, 0]
        self.acceleration = 75
        self.deceleration = 75

        self.health = save_data["health"] if save_data else 20
        self.speed = save_data["speed"] if save_data else 20 * multiplier
        self.max_health = save_data["max_health"] if save_data else 20

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.keys_pressed = pygame.key.get_pressed()

        self.movement(dt)

    def __dict__(self):
        return {
            "x": self.rect.centerx,
            "y": self.rect.centery,
            "width": self.width,
            "height": self.height,
            "health": self.health,
            "max_health": self.max_health,
            "speed": self.speed,
        }

    def movement(self, dt):
        if self.keys_pressed[pygame.K_s]:
            self.velocity[1] += self.acceleration
            if self.velocity[1] > self.speed:
                self.velocity[1] = self.speed
        elif self.keys_pressed[pygame.K_w]:
            self.velocity[1] -= self.acceleration
            if self.velocity[1] < -self.speed:
                self.velocity[1] = -self.speed
        else:
            if self.velocity[1] > 0:
                self.velocity[1] -= self.deceleration
                if self.velocity[1] < 0:
                    self.velocity[1] = 0
            elif self.velocity[1] < 0:
                self.velocity[1] += self.deceleration
                if self.velocity[1] > 0:
                    self.velocity[1] = 0

        if self.keys_pressed[pygame.K_a]:
            self.velocity[0] -= self.acceleration
            if self.velocity[0] < -self.speed:
                self.velocity[0] = -self.speed
        elif self.keys_pressed[pygame.K_d]:
            self.velocity[0] += self.acceleration
            if self.velocity[0] > self.speed:
                self.velocity[0] = self.speed
        else:
            if self.velocity[0] > 0:
                self.velocity[0] -= self.deceleration
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            elif self.velocity[0] < 0:
                self.velocity[0] += self.deceleration
                if self.velocity[0] > 0:
                    self.velocity[0] = 0

        if self.velocity[0] != 0 or self.velocity[1] != 0:
            length = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
            if length > self.speed:
                self.velocity[0] = (self.velocity[0] / length) * self.speed
                self.velocity[1] = (self.velocity[1] / length) * self.speed

        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
