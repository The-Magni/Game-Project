import pygame
import os


ALPHA = (255, 255, 255)


class Ground(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=20, length=150):
        super(Ground, self).__init__()
        self.image = pygame.image.load(os.path.join("images", "ground.png")).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.image = pygame.transform.scale(self.image, (length, width))
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
        self.mask = pygame.mask.from_surface(self.image)
