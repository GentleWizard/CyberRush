import pygame

from States.ui.button import Button


class PausedState:
    def __init__(self, game):
        self.game = game

        self.resume_button = Button(
            x=self.game.width // 2,
            y=self.game.height // 2 - 100,
            width=self.game.width // 2,
            height=self.game.height // 10,
            text="Resume",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.save_button = Button(
            x=self.game.width // 2,
            y=self.resume_button.rect.bottom + 50,
            width=self.resume_button.width,
            height=self.resume_button.height,
            text="Save",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.settings_button = Button(
            x=self.game.width // 2,
            y=self.resume_button.rect.bottom + 50,
            width=self.resume_button.width,
            height=self.resume_button.height,
            text="Settings",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.quit_button = Button(
            x=self.game.width // 2,
            y=self.settings_button.rect.bottom + 50,
            width=self.settings_button.width,
            height=self.settings_button.height,
            text="Quit",
            text_color=(0, 0, 0),
            bg_color=(255, 255, 255),
            font=self.game.font,
            game=self.game,
        )

        self.menu_elements = pygame.sprite.Group(
            self.resume_button,
            self.settings_button,
            self.quit_button,
            self.save_button,
        )

    def update(self, dt):
        self.menu_elements.update(dt)

        self.handle_gui()

    def render(self, screen):
        self.game.states.get("playing").render(screen)
        blur_screen = pygame.Surface((self.game.width, self.game.height))
        blur_screen.set_alpha(200)
        blur_screen.fill((0, 0, 0))
        screen.blit(blur_screen, (0, 0))

        for element in self.menu_elements:
            element.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_state = self.game.states.get("playing")

        if self.resume_button.click_event(rect=self.resume_button.rect):
            self.game.change_state(self.game.states.get("playing"))

        if self.settings_button.click_event(rect=self.settings_button.rect):
            self.game.change_state(self.game.states.get("options"))

        if self.quit_button.click_event(rect=self.quit_button.rect):
            self.game.change_state(self.game.states.get("main_menu"))

        if self.save_button.click_event(rect=self.save_button.rect):
            self.game.states.get("playing").save_game(autosave=False)

    def handle_gui(self, vert_separation=50):
        self.resume_button.update_button(
            x=self.game.width // 2,
            y=self.game.height // 2 - 100,
            width=self.game.width // 2,
            height=self.game.height // 10,
        )
        self.save_button.update_button(
            x=self.game.width // 2,
            y=self.resume_button.rect.bottom + vert_separation,
            width=self.resume_button.width,
            height=self.resume_button.height,
        )

        self.settings_button.update_button(
            x=self.game.width // 2,
            y=self.save_button.rect.bottom + vert_separation,
            width=self.resume_button.width,
            height=self.resume_button.height,
        )
        self.quit_button.update_button(
            x=self.game.width // 2,
            y=self.settings_button.rect.bottom + vert_separation,
            width=self.resume_button.width,
            height=self.resume_button.height,
        )
