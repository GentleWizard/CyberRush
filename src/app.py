import dataclasses
import sys

import pygame

from entity import DataCube, Enemy, Player
from ui.text import HealthBar, PlayerDataCubes
from ui.widgets import Button, Slider


@dataclasses.dataclass
class Settings:
    def __init__(self):
        self.volume = 0.5
        self.fullscreen = False
        self.resolution = (800, 600)
        self.game_play_keybinds = {
            "up": pygame.K_w,
            "left": pygame.K_a,
            "down": pygame.K_s,
            "right": pygame.K_d,
            "ability1": pygame.K_e,
            "ability2": pygame.K_q,
        }
        self.menu_keybinds = {
            "up": pygame.K_w,
            "left": pygame.K_a,
            "down": pygame.K_s,
            "right": pygame.K_d,
            "ability1": pygame.K_e,
            "ability2": pygame.K_q,
        }

    def save(self):
        pass

    def load(self):
        pass

    def set_volume(self, volume):
        self.volume = volume

    def set_fullscreen(self, fullscreen):
        self.fullscreen = fullscreen

    def set_resolution(self, resolution):
        self.resolution = resolution

    def set_game_play_keybinds(self, key, bind):
        self.game_play_keybinds[key] = bind

    def set_menu_keybinds(self, key, bind):
        self.menu_keybinds[key] = bind

    def get_volume(self):
        return self.volume

    def get_fullscreen(self):
        return self.fullscreen

    def get_resolution(self):
        return self.resolution

    def get_game_play_keybinds(self):
        return self.game_play_keybinds

    def get_menu_keybinds(self):
        return self.menu_keybinds


class GameState:
    def __init__(self, game):
        self.screen = game.screen
        self.game = game
        self.settings = game.settings

    def handle_events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def switch_state(self, state):
        if state == "game":
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
        self.game.current_state = self.game.game_state[state]
        pygame.time.delay(100)

    def new_game(self):
        pygame.mouse.set_visible(False)
        self.game.game_state["game"] = PlayingState(self.game)
        self.game.current_state = self.game.game_state["game"]

    def change_resolution(self, width, height):
        self.game.screen = pygame.display.set_mode((width, height), vsync=1)
        self.screen = self.game.screen


class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        self.play_button = Button(
            x=center_x,
            y=center_y - 100,
            width=200,
            height=40,
            text="Play",
            font_size=30,
            bold=True,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            function=lambda: self.new_game(),
        )

        self.settings_button = Button(
            x=center_x,
            y=center_y - 50,
            width=200,
            height=40,
            text="Settings",
            font_size=30,
            bold=True,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            function=lambda: self.switch_state("settings"),
        )

        self.exit_button = Button(
            x=center_x,
            y=center_y,
            width=200,
            height=40,
            text="Exit",
            font_size=30,
            bold=True,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            function=sys.exit,
        )

        self.nav_button_group = pygame.sprite.Group(
            self.play_button, self.settings_button, self.exit_button
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.game.screen.fill((0, 0, 10))

        for button in self.nav_button_group:
            button.draw(self.screen)

        pygame.display.flip()

    def update(self):
        self.nav_button_group.update()


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
        self.player_data_cubes = PlayerDataCubes(0, 0, self.player)

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
        self.keybinds = self.settings.get_game_play_keybinds()

        self.movement_keys = [
            self.keybinds["up"],
            self.keybinds["down"],
            self.keybinds["left"],
            self.keybinds["right"],
        ]
        self.ability_keys = [
            self.keybinds["ability1"],
            self.keybinds["ability2"],
        ]

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

                if event.key == pygame.K_ESCAPE:
                    self.switch_state("pause")

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
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        self.sound_slider = Slider(
            x=center_x,
            y=center_y - 100,
            width=200,
            height=30,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            text=str(self.settings.get_volume()) * 100,
            label="Volume",
            label_bold=True,
            label_colour=(255, 255, 255),
            handle_size=15,
            handle_colour=(255, 255, 255),
        )

        self.back_button = Button(
            x=center_x,
            y=center_y,
            width=200,
            height=40,
            text="Back",
            font_size=30,
            bold=True,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            function=lambda: self.switch_state("menu"),
        )

        self.nav_button_group = pygame.sprite.Group(
            self.back_button,
        )
        self.slider_group = pygame.sprite.Group(
            self.sound_slider,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.game.screen.fill((0, 0, 10))

        self.sound_slider.draw(self.screen)
        self.back_button.draw(self.screen)

        pygame.display.flip()

    def update(self):
        self.nav_button_group.update()
        self.slider_group.update()
        self.settings.set_volume(self.sound_slider.get_value())
        self.sound_slider.set_text(str(self.settings.get_volume()) * 100)


class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        self.resume_button = Button(
            x=center_x,
            y=center_y - 100,
            width=200,
            height=40,
            text="Resume",
            font_size=30,
            bold=True,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            function=lambda: self.switch_state("game"),
        )

        self.restart_button = Button(
            x=center_x,
            y=center_y - 50,
            width=200,
            height=40,
            text="Restart",
            font_size=30,
            bold=True,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            function=lambda: self.new_game(),
        )

        self.quit_button = Button(
            x=center_x,
            y=center_y,
            width=200,
            height=40,
            text="Quit",
            font_size=30,
            bold=True,
            colour=(100, 175, 200),
            hover_colour=(150, 200, 225),
            function=lambda: self.switch_state("menu"),
        )

        self.nav_button_group = pygame.sprite.Group(
            self.resume_button, self.quit_button, self.restart_button
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.game.screen.fill((0, 0, 10))

        for button in self.nav_button_group:
            button.draw(self.screen)

        pygame.display.flip()

    def update(self):
        self.nav_button_group.update()


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
        # Game state
        self.screen = pygame.display.set_mode((width, height), vsync=1)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.game_state = {
            "menu": MenuState(self),
            "game": PlayingState(self),
            "settings": SettingsState(self),
            "pause": PauseState(self),
            "game_over": GameOverState(self),
        }
        self.current_state = self.game_state["menu"]

    def handle_events(self):
        self.current_state.handle_events()

    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw()

    def run(self):
        while True:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = CyberRush(800, 600, "CyberRush")
    game.run()
