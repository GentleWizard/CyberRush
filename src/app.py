import sys

import pygame

from entities.data_cube import DataCube
from entities.enemy import Enemy
from entities.player import Player
from ui.text.data_cubes import PlayerDataCubes
from ui.text.health import HealthBar


class GameState:
    def __init__(self, game):
        self.screen = game.screen
        self.game = game

    def handle_events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.game.screen.fill((0, 0, 10))
        pygame.display.flip()


class PlayingState(GameState):
    def __init__(self, game):
        super().__init__(game)

        # Entities
        self.player = Player(100, 100)
        self.data_cube = DataCube()
        self.data_cube.randomise_position()
        self.enemy = Enemy(200, 200)

        # UI
        self.player_health_bar = HealthBar(
            self.player.rect.center[0], (self.player.rect.center[1] - 10), self.player
        )
        self.player_data_cubes = PlayerDataCubes(0, 20, self.player)

        # Groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.data_cube_group = pygame.sprite.Group(self.data_cube)
        self.enemy_group = pygame.sprite.Group(self.enemy)

        self.entity_group = pygame.sprite.Group(
            self.data_cube_group,
            self.enemy_group,
            self.player_group,
        )

        self.text_group = pygame.sprite.Group(
            self.player_health_bar, self.player_data_cubes
        )
        self.button_group = pygame.sprite.Group()

        self.ui_group = pygame.sprite.Group(
            self.text_group,
            self.button_group,
        )

        # Keybinds
        self.movement_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
        self.ability_keys = [pygame.K_e, pygame.K_q]

    def handle_events(self):
        if pygame.sprite.groupcollide(
            self.player_group, self.data_cube_group, False, True
        ):
            if not self.data_cube.alive():
                self.data_cube = DataCube()
                self.data_cube_group.add(self.data_cube)
                if self.data_cube_group not in self.entity_group:
                    self.entity_group.add(self.data_cube_group)
            self.player.pickup_data_cube()
            self.data_cube.randomise_position()

        if pygame.sprite.groupcollide(
            self.player_group, self.enemy_group, False, False
        ):
            self.enemy.attack(self.player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in self.movement_keys:
                    self.player.direction.append(event.key)

                if event.key == pygame.K_e:
                    self.player.health -= 10
                    print(self.player.health)
                elif event.key == pygame.K_q:
                    self.player.health += 10
                    print(self.player.health)

            if event.type == pygame.KEYUP:
                if event.key in self.movement_keys:
                    for direction in self.player.direction:
                        if event.key == direction:
                            self.player.direction.remove(direction)

    def update(self):
        self.entity_group.update()
        self.ui_group.update()

    def draw(self):
        self.screen.fill((0, 0, 10))

        # entities
        self.entity_group.draw(self.screen)
        self.ui_group.draw(self.screen)

        # UI
        for ui in self.ui_group:
            ui.draw(self.screen)

        pygame.display.flip()


class SettingsState(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.game.screen.fill((0, 0, 10))
        pygame.display.flip()


class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.game.screen.fill((0, 0, 10))
        pygame.display.flip()


class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.game.screen.fill((0, 0, 10))
        pygame.display.flip()


class CyberRush:
    def __init__(self, width, height, title):
        # Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), vsync=1)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.window_width = width
        self.window_height = height

        # Game state
        self.game_state = {
            "menu": MenuState(self),
            "game": PlayingState(self),
            "settings": SettingsState(self),
            "pause": PauseState(self),
            "game_over": GameOverState(self),
        }
        self.current_state = self.game_state["game"]

    def handle_events(self):
        self.current_state.handle_events()

    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw()

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
