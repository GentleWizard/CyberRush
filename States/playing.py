import os
import pickle

import pygame

from .Entities.player import Player
from .ui.text import Text


class PlayingState:
    def __init__(self, game, game_data=None):
        self.game = game
        self.game_data = game_data

        self.player_group = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()

        self.player = Player(
            self.game,
            self.game_data["player"]["x"] if self.game_data else self.game.width // 2,
            self.game_data["player"]["y"] if self.game_data else self.game.height // 2,
            self.game_data["player"]["width"] if self.game_data else 50,
            self.game_data["player"]["height"] if self.game_data else 50,
            save_data=self.game_data["player"] if self.game_data else None,
        )
        self.player_group.add(self.player)

        self.last_save = 0
        self.save_interval = 120

        self.time_played = self.game_data["time_played"] if self.game_data else 0
        self.last_update_time = 0

        self.new_game = False if game_data else True

        self.health_text = Text(
            x=10,
            y=10,
            width=100,
            height=50,
            game=self.game,
            text=f"Health: {self.player.health}",
            font_size=20,
            text_color=(255, 255, 255),
        )

        self.ui_group.add(self.health_text)

    def update(self, dt):
        self.player_group.update(dt)
        self.ui_group.update(dt)

        seconds_passed = self.calculate_time_played()

        self.last_save += seconds_passed
        if self.last_save >= self.save_interval:
            self.save_game(autosave=True)
            self.last_save = 0

    def render(self, screen):
        for player in self.player_group:
            player.draw(screen)

        self.ui_group.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state(self.game.states.get("paused"))

            if event.key == pygame.K_q:
                self.player.health -= 10

            if event.key == pygame.K_e:
                self.player.health += 10

    def save_game(self, autosave=True):
        save_number = 1
        for file in os.listdir("saves"):
            for char in file:
                if char.isdigit():
                    if self.new_game:
                        save_number = int(char) + 1
                    else:
                        save_number = int(char)

        game_data = {
            "filename": f"savegame{save_number}" if not autosave else "autosave",
            "player": self.player.__dict__(),
            "time_played": self.time_played,
        }
        if autosave:
            with open(f"saves/autosave.pkl", "wb") as f:
                pickle.dump(game_data, f)
                self.save = "autosave"
        else:
            with open(f"saves/savegame{save_number}.pkl", "wb") as f:
                pickle.dump(game_data, f)
                self.save = f"savegame{save_number}"

    def calculate_time_played(self):
        current_time = pygame.time.get_ticks()
        seconds_passed = (current_time - self.last_update_time) / 1000
        self.time_played += seconds_passed
        self.last_update_time = current_time
        return seconds_passed

    def handle_gui(self):
        self.health_text.update_text(x=10, y=10, text=f"Health: {self.player.health}")
