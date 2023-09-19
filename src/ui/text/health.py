from .text import Text


def calculate_health_colour(health_percentage):
    r = 255 * (1 - health_percentage) * 2
    g = 255 * health_percentage
    b = 0
    r = min(r, 255)
    g = min(g, 255)
    b = min(b, 255)
    return r, g, b


class HealthBar(Text):
    def __init__(self, x, y, player):
        super().__init__(x, y)
        self.player = player
        self.content = f"{self.player.health}"
        self.image = self.font.render(self.content, True, self.colour)

        self.rect = self.image.get_rect()
        self.health_percentage = self.player.health / self.player.max_health

        self.width = self.rect.width
        self.height = self.rect.height
        self.health_colour = (0, 255, 0)

    def update(self):
        self.content = f"{self.player.health}"

        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.x = self.player.rect.center[0] - (self.width // 1.5)
        self.rect.y = self.player.rect.center[1] - (self.height * 1.6)

        if self.player.health <= self.player.max_health:
            self.health_percentage = self.player.health / self.player.max_health
            self.health_colour = calculate_health_colour(self.health_percentage)
            self.image = self.font.render(self.content, True, self.health_colour)
