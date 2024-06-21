import pygame
import math
import random
from throwable import Throwable

SPEED = 30
PI = 3.14
ANI = 3
TOTAL_FRAMES = 2 * ANI


class Iceball(Throwable):
    def __init__(self, xloc, yloc, img, scale, knight, firewizard):
        super().__init__(xloc, yloc, img, scale)
        if self.distance(knight) < self.distance(firewizard):
            self.directionx = (knight.rect.x - self.rect.x) / self.distance(knight)
            self.directiony = (knight.rect.y - self.rect.y) / self.distance(knight)
        else:
            self.directionx = (firewizard.rect.x - self.rect.x) / self.distance(
                firewizard
            )
            self.directiony = (firewizard.rect.y - self.rect.y) / self.distance(
                firewizard
            )
        self.movex = self.directionx * SPEED
        self.movey = self.directiony * SPEED
        if self.directionx < 0:
            self.left = False
        else:
            self.left = True

        self.is_reflected = False
        self.can_freeze = random.choice([1, 1, 1, 1, 1])

    def gravity(self):
        if self.is_reflected:
            super().gravity()

    def distance(self, character):
        return math.sqrt(
            math.pow((self.rect.centerx - character.rect.centerx), 2)
            + math.pow((self.rect.centery - character.rect.centery), 2)
        )
    
    def hit_knight(self, knight):
        if self.rect.colliderect(knight.attack_range) and knight.is_attacking:
            self.movex = -self.movex
            self.is_reflected = True

    def update(self, worldy, worldx, knight):
        self.rect.x += self.movex
        self.rect.y += self.movey
        if 0 < self.rect.y < worldy and 0 < self.rect.x < worldx:
            self.frame += 1
            if self.frame >= TOTAL_FRAMES:
                self.frame = 0
            try:
                angle = math.atan(-self.movey / self.movex)
            except ZeroDivisionError:
                if self.movey > 0:
                    angle = 3 / 2 * PI
                else:
                    angle = PI / 2
            if self.left:
                self.image = pygame.transform.rotate(
                    self.images[self.frame // ANI], angle * 180 / 3.14
                )
            else:
                self.image = pygame.transform.rotate(
                    pygame.transform.flip(self.images[self.frame // ANI], True, False),
                    angle * 180 / 3.14,
                )
        else:
            self.kill()
        self.gravity()
        self.hit_knight(knight)
