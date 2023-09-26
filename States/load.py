import os
import pickle

import pygame

from .playing import PlayingState
from .ui.button import Button


class LoadState:
    def __init__(self, game):
        self.game = game
        self.menu_elements = pygame.sprite.Group()

        self.back_button = Button(
            x=self.game.width // 2,
            y=self.game.height // 2 * 1.8,
            width=self.game.width // 2,
            height=self.game.height // 10,
            text="Back",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.menu_elements.add(self.back_button)

        self.no_saves_font = pygame.font.SysFont("Arial", 50)
        self.no_saves_text = self.no_saves_font.render(
            "No saves found!", True, (255, 255, 255)
        )
        self.text_rect = self.no_saves_text.get_rect(
            center=(self.game.width // 2, self.game.height // 3)
        )

        self.saves = []
        self.check_for_saves()

        self.saves_group = pygame.sprite.Group()

    def update(self, dt):
        self.menu_elements.update(dt)
        self.saves_group.update(dt)


        self.handle_gui()

    def render(self, screen):
        for element in self.menu_elements:
            element.draw(screen)
        if not self.saves:
            self.game.screen.blit(self.no_saves_text, self.text_rect)
        else:
            for i, save in enumerate(self.saves):
                with open(f"saves/{save}", "rb") as f:
                    save_data = pickle.load(f)
                    filename = save_data["filename"]
                    distance = i * self.game.height // 10 + i * 10

                    load_button = Button(
                        x=self.game.width // 2,
                        y=self.game.height // 3 + distance,
                        width=self.game.width // 2,
                        height=self.game.height // 10,
                        text=filename,
                        text_color=(0, 0, 0),
                        bg_color=(255, 255, 255),
                        font=self.game.font,
                        game=self.game,
                    )

                    self.saves_group.add(load_button)

            for button in self.saves_group:
                button.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game.previous_state is None:
                    self.game.change_state(self.game.states.get("main_menu"))
                else:
                    self.game.change_state(self.game.previous_state)

        if self.back_button.click_event(rect=self.back_button.rect):
            self.game.change_state(self.game.previous_state)

        for button in self.saves_group:
            if button.click_event(rect=button.rect):
                with open(f"saves/{button.content}.pkl", "rb") as f:
                    save_data = pickle.load(f)
                    self.game.states["playing"] = PlayingState(self.game, save_data)
                    self.game.change_state(self.game.states.get("playing"))

    def check_for_saves(self):
        self.back_button.set_active(False)
        if not os.path.exists("saves"):
            os.makedirs("saves")
        for file in os.listdir("saves"):
            if file.endswith(".pkl"):
                self.saves.append(file)
        self.back_button.set_active(True)

    def handle_gui(self):
        self.back_button.update_button(
            x=self.game.width // 2,
            y=self.game.height // 2 * 1.8,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )

