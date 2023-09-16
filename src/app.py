import random
import sys

import pygame
from pygame.sprite import Sprite


class CyberRush:
    def __init__(self, width, height, title):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        self.width = width
        self.height = height
        self.player = Player(100, 100)
        self.data_cube = DataCube(width, height)

        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.data_cube_group = pygame.sprite.Group(self.data_cube)

        self.movement_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]

    def handle_events(self):
        if pygame.sprite.groupcollide(
            self.player_group, self.data_cube_group, False, True
        ):
            self.player.pickup_data_cube()
            self.data_cube = DataCube(self.width, self.height)
            self.data_cube_group.add(self.data_cube)
            print(self.player.data_cubes)

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

    def draw(self):
        self.screen.fill((0, 0, 10))  # Keep at top of draw method

        self.screen.blit(self.data_cube.sprite, self.data_cube.rect)
        self.screen.blit(self.player.sprite, self.player.rect)

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

    def update(self):
        if self.data_cubes_cooldown > 0:
            self.data_cubes_cooldown -= 1
        self.movement()

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


if __name__ == "__main__":
    game = CyberRush(800, 600, "CyberRush")
    game.run()
