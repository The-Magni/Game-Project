import pygame
import math
import os

ANI = 4
TOTAL_FRAMES = 2 * ANI


class Throwable(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img, scale):
        super().__init__()
        self.images = []
        for i in range(1, 3):
            image = pygame.image.load(os.path.join("images", img + str(i) + ".png"))
            image = pygame.transform.scale_by(image, scale)
            self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = xloc
        self.rect.y = yloc
        self.movex = 0
        self.movey = -7
        self.mask = pygame.mask.from_surface(self.image)
        self.left = False
        self.frame = 0

    def hit_ground(self, grounds):
        for ground in grounds:
            if self.mask.overlap(
                ground.mask, (ground.rect.x - self.rect.x, ground.rect.y - self.rect.y)
            ):
                self.kill()

    def gravity(self):
        self.movey += 1

    def move(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

    def update(self, worldx, worldy, grounds):
        if self.rect.y < worldy and self.rect.x < worldx and self.rect.x > 0:
            self.frame += 1
            if self.frame >= TOTAL_FRAMES:
                self.frame = 0
            if not self.left:
                self.movex = 30
                angle = math.atan(-self.movey / self.movex)
                self.image = pygame.transform.rotate(
                    self.images[self.frame // ANI], angle * 180 / 3.14
                )
            else:
                self.movex = -30
                angle = math.atan(-self.movey / self.movex)
                self.image = pygame.transform.rotate(
                    pygame.transform.flip(self.images[self.frame // ANI], True, False),
                    angle * 180 / 3.14,
                )
        else:
            self.kill()
            self.firing = False

        self.hit_ground(grounds)
        self.move()
        self.gravity()
