import pygame
import os


ALPHA = (0, 0, 0)


class Icecube(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        img = pygame.image.load(os.path.join("images", "icecube.png")).convert_alpha()
        img.set_colorkey(ALPHA)
        self.image = pygame.transform.scale(
            img, (75, 100)
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = character.rect.centerx
        self.rect.bottom = character.rect.bottom
        self.character = character
        self.exist_time = 10

    def update(self):
        if self.exist_time:
            self.rect.centerx = self.character.rect.centerx
            self.rect.bottom = self.character.rect.bottom
            self.exist_time -= 1
        else:
            self.kill()
            self.character.is_freeze = False