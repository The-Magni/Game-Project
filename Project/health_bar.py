import pygame


RED = pygame.Color((255, 0, 0))
GREEN = pygame.Color((0, 255, 0))


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, width, height, sprite):
        super(HealthBar, self).__init__()
        self.x = sprite.rect.centerx
        self.y = sprite.rect.top - 5
        self.width = width
        self.height = height
        self.sprite = sprite

    def appear(self, surf):
        ratio = self.sprite.health / self.sprite.max_health
        if self.sprite.health > 0:
            pygame.draw.rect(
                surf,
                RED,
                pygame.Rect(
                    self.x - self.width / 2,
                    self.y - self.height / 2,
                    self.width,
                    self.height,
                ),
            )
            pygame.draw.rect(
                surf,
                GREEN,
                pygame.Rect(
                    self.x - self.width / 2,
                    self.y - self.height / 2,
                    self.width * ratio,
                    self.height,
                ),
            )

    def update(self):
        self.x = self.sprite.rect.centerx
        self.y = self.sprite.rect.top - 5
