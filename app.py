import sys

import pygame

from options import Settings
from States.game_over import GameOverState
from States.load import LoadState
from States.main_menu import MainMenuState
from States.options import OptionsState
from States.paused import PausedState

# TODO: Look at Docs for usful functions

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps_cap = self.settings.get_fps_cap()
        self.width = self.settings.get_width()
        self.height = self.settings.get_height()

        self.resolution = (self.width, self.height)
        
        info = pygame.display.Info()
        self.screen_res = (info.current_w, info.current_h)
        self.settings.set_height(info.current_h)
        self.settings.set_width(info.current_w)

        if self.settings.get_fullscreen():
            self.flags = (
                pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN | pygame.NOFRAME
            )
            self.screen = pygame.display.set_mode(
                (self.settings.get_width(), self.settings.get_height()), self.flags
            )
        else:
            self.flags = pygame.HWACCEL | pygame.HWSURFACE | pygame.NOFRAME
            self.screen = pygame.display.set_mode(
                (self.settings.get_width() //2 , self.settings.get_height() //2), self.flags
            )

        pygame.display.set_caption(self.settings.get_title())
        pygame.display.set_allow_screensaver(self.settings.allow_screensaver())
        


        self.font = "Assets/Fonts/Roboto-Regular.ttf"

        self.left_clicked = False
        self.right_clicked = False
        self.left_click_held = False
        self.right_click_held = False

        self.hovered = False

        self.previous_state = None

        self.vsync = True

        self.states = {
            "playing": None,
            "paused": PausedState(self),
            "game_over": GameOverState(self),
            "main_menu": MainMenuState(self),
            "options": OptionsState(self),
            "credits": None,
            "load": LoadState(self),
        }

        self.current_state = self.states.get("main_menu")

    def run(self):
        while self.running:
            self.clock.tick(self.fps_cap)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_clicked = True
                    self.left_click_held = True
                if event.button == 3:
                    self.right_clicked = True
                    self.right_click_held = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_click_held = False
                if event.button == 3:
                    self.right_click_held = False

            self.current_state.handle_events(event)
            self.left_clicked = False
            self.right_clicked = False

            if event.type == pygame.QUIT:
                self.exit_game()

    def update(self):
        self.current_state.update(dt=self.clock.tick(self.fps_cap) / 1000)

        self.width = pygame.display.get_surface().get_size()[0]
        self.height = pygame.display.get_surface().get_size()[1]

    def draw(self):
        self.screen.fill((0, 0, 10))

        self.current_state.render(self.screen)

        pygame.display.flip()

    def change_state(self, state):
        self.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.previous_state = self.current_state
        if state != self.current_state and state in self.states.values():
            if state == self.states.get("playing"):
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)
            self.current_state = state

    def change_cursor(self, cursor):
        pygame.mouse.set_cursor(cursor)

    def exit_game(self):
        self.settings.save()
        self.running = False
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
