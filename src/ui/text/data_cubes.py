from .text import Text


class PlayerDataCubes(Text):
    def __init__(self, x, y, player):
        super().__init__(x, y)
        self.player = player
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.image = self.font.render(self.content, True, self.colour)

    def update(self):
        self.content = f"Data Cubes: {self.player.data_cubes}"
        self.image = self.font.render(self.content, True, self.colour)
