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
            y=self.game.height // 2 // 2.5,
            text="Back",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.fullscreen_button = Button(
            y=self.game.height // 2 // 2,
            text="Play Fullscreen",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.volume = Slider(
            x=self.game.width // 2,
            y=self.fullscreen_button.rect.top - self.fullscreen_button.height // 1.5,
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
            self.monitor_info = (self.game.settings.get_width(), self.game.settings.get_height())
            
            if not pygame.display.is_fullscreen():
                pygame.display.set_mode(
                    (self.monitor_info), self.game.screen.get_flags() | pygame.FULLSCREEN
                )
                self.game.settings.set_fullscreen(True)
            else:
                pygame.display.set_mode(
                    (self.monitor_info[0]//2, self.monitor_info[1]//2),
                    self.game.screen.get_flags() & ~pygame.FULLSCREEN,
                )
                self.game.settings.set_fullscreen(False)

    def handle_gui(self):
        self.back_button.update_button(
            x=self.game.width // 2,
            y=self.game.height // 2 * 1.8,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )
        self.fullscreen_button.update_button(
            x=self.game.width // 2,
            y=self.game.height // 2,
            width=self.back_button.width,
            height=self.back_button.height,
            text=f"Play {'Windowed' if not pygame.display.is_fullscreen() else 'Fullscreen'}",
        )


    def __repr__(self):
        return "OptionsState"
