from .entity import Entity


class Enemy(Entity):
    def __init__(self, x, y, colour=(255, 0, 0)):
        super().__init__(x, y, colour)

        self.hitdelay = 0
        self.damage = 10
        self.speed = 3

    def update(self):
        if self.hitdelay > 0:
            self.hitdelay -= 1

        self.ai()

    def attack(self, player):
        if self.hitdelay > 0:
            return
        player.health -= self.damage + player.data_cubes
        self.hitdelay = 65

    def ai(self):
        pass
