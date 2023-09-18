import sys

import pygame

from entities import DataCube, Enemy, Player
from UI import player_Data_Cubes, player_Health_Bar


class CyberRush:
    def __init__(self, width, height, title):
        # Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), vsync=1)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        self.width = width
        self.height = height

        # Entities
        self.player = Player(100, 100)
        self.data_cube = DataCube(width, height)
        self.data_cube.randomise_position()
        self.enemy = Enemy(200, 200)

        # UI
        self.player_health_bar = player_Health_Bar(
            self.player.rect.center[0], (self.player.rect.center[1] - 10), self.player
        )
        self.player_data_cubes = player_Data_Cubes(0, 20, self.player)

        # Groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.data_cube_group = pygame.sprite.Group(self.data_cube)
        self.ui_group = pygame.sprite.Group(
            self.player_health_bar, self.player_data_cubes
        )
        self.enemy_group = pygame.sprite.Group(self.enemy)

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
            self.data_cube.randomise_position()

        if pygame.sprite.groupcollide(
            self.player_group, self.enemy_group, False, False
        ):
            self.enemy.attack(self.player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in self.movement_keys:
                    self.player.direction.append(event.key)

                if event.key == pygame.K_e:
                    self.player.health -= 10
                    print(self.player.health)
                elif event.key == pygame.K_q:
                    self.player.health += 10

            if event.type == pygame.KEYUP:
                if event.key in self.movement_keys:
                    for direction in self.player.direction:
                        if event.key == direction:
                            self.player.direction.remove(direction)

    def update(self):
        self.player_group.update()
        self.data_cube_group.update()
        self.ui_group.update()
        self.enemy_group.update()

    def draw(self):
        self.screen.fill((0, 0, 10))  # Keep at top of draw method

        # entities
        self.screen.blit(self.data_cube.sprite, self.data_cube.rect)
        self.screen.blit(self.player.sprite, self.player.rect)
        self.screen.blit(self.enemy.sprite, self.enemy.rect)

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


if __name__ == "__main__":
    game = CyberRush(800, 600, "CyberRush")
    game.run()
