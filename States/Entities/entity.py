from pygame.sprite import Sprite


class Entity(Sprite):
    def __init__(self, game, x, y, width, height):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_pos(self):
        return self.x, self.y

    def dimensions(self):
        return self.width, self.height
