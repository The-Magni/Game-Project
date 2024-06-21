import pygame
import os
import math
from character import Character

ANI = 4
TOTAL_FRAMES = 3 * ANI
SPEED = 2


class Golem(Character):
    def __init__(self, max_heath, xloc, yloc):
        super().__init__(max_health=max_heath)
        for i in range(4):
            img = pygame.image.load(
                os.path.join("images", "golem" + str(i) + ".png")
            ).convert_alpha()
            img = pygame.transform.scale_by(img, 3)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_bounding_rect()
        self.rect.x = xloc
        self.rect.y = yloc
        self.frame = 0
        self.see_range = pygame.Rect(0, 0, 0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, grounds, knight, firewizard, fireballs):
        super().update()
        self.gravity()
        self.move(knight, firewizard)
        self.hit_ground(grounds)
        self.hit_fireball(fireballs)
        self.hit_knight(knight)

    def gravity(self):
        super().gravity()
        if not self.is_jumping:
            self.is_jumping = True

    def distane(self, character):
        return math.sqrt(
            math.pow((self.rect.centerx - character.rect.centerx), 2)
            + math.pow((self.rect.centery - character.rect.centery), 2)
        )

    def hit_fireball(self, fireballs):
        if pygame.sprite.spritecollide(
            self, fireballs, dokill=True, collided=pygame.sprite.collide_mask
        ):
            self.health -= 4

    def move(self, knight, firewizard):
        self.see_range = self.rect.scale_by(7, 1.5)
        self.see_range.centerx = self.rect.centerx
        self.see_range.bottom = self.rect.bottom + 10

        self.frame += 1
        if self.frame >= TOTAL_FRAMES:
            self.frame = 0
        if self.movex > 0:
            self.image = self.images[self.frame // ANI]
        if self.movex < 0:
            self.image = pygame.transform.flip(
                self.images[self.frame // ANI], True, False
            )
        if self.see_range.colliderect(knight.rect) and self.see_range.colliderect(
            firewizard.rect
        ):
            if self.distane(knight) < self.distane(firewizard):
                if self.rect.centerx < knight.rect.centerx:
                    self.movex = SPEED
                elif self.rect.centerx > knight.rect.centerx:
                    self.movex = -SPEED
                else:
                    self.movex = 0
            else:
                if self.rect.centerx < firewizard.rect.centerx:
                    self.movex = SPEED
                elif self.rect.centerx > firewizard.rect.centerx:
                    self.movex = -SPEED
                else:
                    self.movex = 0
        elif self.see_range.colliderect(knight.rect):
            if self.distane(knight) < self.distane(firewizard):
                if self.rect.centerx < knight.rect.centerx:
                    self.movex = SPEED
                elif self.rect.centerx > knight.rect.centerx:
                    self.movex = -SPEED
                else:
                    self.movex = 0
        elif self.see_range.colliderect(firewizard.rect):
            if self.rect.centerx < firewizard.rect.centerx:
                self.movex = SPEED
            elif self.rect.centerx > firewizard.rect.centerx:
                self.movex = -SPEED
            else:
                self.movex = 0
        else:
            self.movex = 0
