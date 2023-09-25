import pygame

from .ui.button import Button
from .ui.slider import Slider


class OptionsState:
    def __init__(self, game):
        self.previous_width = None
        self.previous_height = None
        self.game = game
        self.menu_elements = pygame.sprite.Group()

        self.back_button = Button(
            y=self.game.height // 1.2,
            text="Back",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.fullscreen_button = Button(
            y=self.back_button.rect.top - 100,
            text="Play Fullscreen",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.volume = Slider(
            x=self.game.width // 2,
            y=self.fullscreen_button.rect.top - 100,
            width=self.game.width // 2,
            height=50,
            label="Volume",
            text="Valume",
            text_color=(0, 0, 0),
            label_color=(255, 255, 255),
            track_color=(255, 255, 255),
            slider_color=(100, 100, 100),
            default_value=self.game.settings.get_volume(),
            font=self.game.font,
            game=self.game,
        )

        self.menu_elements.add(
            self.back_button,
            self.fullscreen_button,
            self.volume,
        )

    def update(self, dt):
        self.menu_elements.update(dt)
        self.game.settings.set_volume(self.volume.value)

        self.handle_gui()

    def render(self, screen):
        for element in self.menu_elements:
            element.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game.previous_state is None:
                    self.game.change_state(self.game.states.get("main_menu"))
                else:
                    self.game.change_state(self.game.previous_state)

        if self.back_button.click_event(rect=self.back_button.rect):
            if self.game.previous_state is None:
                self.game.change_state(self.game.states.get("main_menu"))
            else:
                self.game.change_state(self.game.previous_state)

        if self.fullscreen_button.click_event(rect=self.fullscreen_button.rect):
            if not pygame.display.is_fullscreen():
                pygame.display.set_mode(
                    (1280, 720), self.game.screen.get_flags() | pygame.FULLSCREEN
                )
                self.game.settings.set_fullscreen(True)
            else:
                pygame.display.set_mode(
                    self.game.resolution,
                    self.game.screen.get_flags() & ~pygame.FULLSCREEN,
                )
                self.game.settings.set_fullscreen(False)

    def handle_gui(self):
        self.back_button.update_button(
            x=self.game.width // 2,
            y=self.game.height - 100,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )
        self.fullscreen_button.update_button(
            x=self.game.width // 2,
            y=self.back_button.rect.top - 100,
            width=self.back_button.width,
            height=self.back_button.height,
        )
        self.volume.update_slider(
            x=self.game.width // 2,
            y=self.fullscreen_button.rect.top - 100,
            width=self.game.width // 2,
            height=50,
            inner_text=f"Volume: {self.volume.value}%",
        )

    def __repr__(self):
        return "OptionsState"
