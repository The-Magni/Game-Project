import pygame
import os

ANI = 1
TOTAL_FRAMES = 10 * ANI


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = []
        for i in range(1, 11):
            img = pygame.image.load(
                os.path.join("images", "Explosion_" + str(i) + ".png")
            )
            img = pygame.transform.scale_by(img, 0.15)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0

    def update(self):
        center = self.rect.center
        self.image = self.images[self.frame // ANI]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame += 1
        if self.frame >= TOTAL_FRAMES:
            self.kill()
