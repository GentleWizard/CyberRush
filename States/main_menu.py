import pygame

from .load import LoadState
from .playing import PlayingState
from .ui.button import Button


class MainMenuState:
    def __init__(self, game):
        self.game = game

        self.menu_elements = pygame.sprite.Group()

        self.resume_button = Button(
            y=self.game.height // 2 // 2,
            text="Resume Game",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )
        self.load_button = Button(
            y=self.resume_button.rect.top + self.resume_button.height // 1.5,
            text="Load Game",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )
        self.new_game_button = Button(
            y=self.load_button.rect.bottom + self.load_button.height // 1.5,
            text="New Game",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.settings_button = Button(
            y=self.new_game_button.rect.bottom + self.new_game_button.height // 1.5,
            text="Settings",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.exit_button = Button(
            y=self.settings_button.rect.bottom + self.settings_button.height // 1.5,
            text="Exit",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.menu_elements.add(
            self.exit_button,
            self.settings_button,
            self.new_game_button,
            self.resume_button,
            self.load_button,
        )

    def update(self, dt):
        self.menu_elements.update(dt)

        self.handle_gui()

    def render(self, screen):
        for element in self.menu_elements:
            element.draw(screen)

    def handle_events(self, event):
        if self.game.states.get("playing") is not None:
            self.resume_button.set_active(True)
            if self.resume_button.click_event(rect=self.resume_button.rect):
                self.game.change_state(self.game.states.get("playing"))
        else:
            self.resume_button.set_active(False)

        if self.new_game_button.click_event(rect=self.new_game_button.rect):
            self.game.states["playing"] = PlayingState(self.game)
            self.game.change_state(self.game.states.get("playing"))

        if self.settings_button.click_event(rect=self.settings_button.rect):
            self.game.change_state(self.game.states.get("options"))

        if self.load_button.click_event(rect=self.load_button.rect):
            self.game.states["load"] = LoadState(self.game)
            self.game.change_state(self.game.states.get("load"))

        if self.exit_button.click_event(rect=self.exit_button.rect):
            self.game.exit_game()

        if event.type == pygame.key.get_pressed():
            if event.key == pygame.K_f:
                if pygame.display.is_fullscreen():
                    pygame.display.set_mode(
                        self.game.resolution,
                        self.game.screen.get_flags() & ~pygame.FULLSCREEN,
                    )
                    self.game.settings.set_fullscreen(False)
                else:
                    pygame.display.set_mode(
                        (1280, 720),
                        self.game.screen.get_flags() | pygame.FULLSCREEN,
                    )
                    self.game.settings.set_fullscreen(True)

    def handle_gui(self):
        self.resume_button.update_button(
            x=self.game.width // 2,
            y=self.game.height // 2 // 2,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )
        self.load_button.update_button(
            x=self.game.width // 2,
            y=self.resume_button.rect.bottom + self.resume_button.height // 1.5,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )
        self.new_game_button.update_button(
            x=self.game.width // 2,
            y=self.load_button.rect.bottom + self.load_button.height // 1.5,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )
        self.settings_button.update_button(
            x=self.game.width // 2,
            y=self.new_game_button.rect.bottom + self.new_game_button.height // 1.5,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )
        self.exit_button.update_button(
            x=self.settings_button.rect.centerx,
            y=self.settings_button.rect.bottom + self.settings_button.height // 1.5,
            width=self.settings_button.width,
            height=self.settings_button.height,
        )

    def __repr__(self):
        return "MainMenuState"
