import random

from .entity import Entity


class DataCube(Entity):
    def __init__(self, colour=(0, 255, 0), x=0, y=0):
        super().__init__(x, y, colour)

    def randomise_position(self):
        self.rect.x = random.randint(50, self.game_width - 50)
        self.rect.y = random.randint(50, self.game_height - 50)
