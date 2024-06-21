import pygame
import os
from character import Character
from throwable import Throwable


ANI = 4
TOTAL_FRAMES = 4 * ANI
ANI_ATCK = 4
TOTAL_FRAMES_ATCK = 3 * ANI_ATCK


class Wizard(Character):
    def __init__(self, max_health, img):
        super().__init__(max_health)
        for i in range(1, 5):
            image = pygame.image.load(
                os.path.join("images", img + "_run_" + str(i) + ".png")
            ).convert_alpha()
            image = pygame.transform.scale_by(image, 0.2)
            self.images.append(image)

        for i in range(1, 4):
            image = pygame.image.load(
                os.path.join("images", img + "_attack_" + str(i) + ".png")
            ).convert_alpha()
            image = pygame.transform.scale_by(image, 0.2)
            self.attack_images.append(image)

        self.image = self.images[0]
        self.rect = self.image.get_bounding_rect()
        self.rect.x = 200
        self.rect.y = 700
        self.mask = pygame.mask.from_surface(self.image)

        self.frame = 0
        self.attack_frame = 0

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def jump(self):
        if not self.is_jumping:
            self.is_falling = False
            self.is_jumping = True

        if self.is_jumping and not self.is_falling:
            self.is_falling = True
            self.movey -= 20

    def attack(self):
        if self.is_attacking:
            if self.attack_frame >= TOTAL_FRAMES_ATCK:
                self.attack_frame = 0
                self.is_attacking = False
            if self.left:
                self.image = pygame.transform.flip(
                    self.attack_images[self.attack_frame // ANI_ATCK], True, False
                )
            else:
                self.image = self.attack_images[self.attack_frame // ANI_ATCK]
            self.attack_frame += 1

    def hit_golem(self, golems):
        if pygame.sprite.spritecollide(
            self, golems, dokill=False, collided=pygame.sprite.collide_mask
        ):
            self.health -= 1

    def update(self, grounds, golems, iceballs):
        if self.movex != 0:
            self.is_jumping = True
            self.frame += 1
            self.is_attacking = False
        if self.frame >= TOTAL_FRAMES:
            self.frame = 0

        if self.movex > 0:
            self.image = self.images[self.frame // ANI]
            self.left = False
        elif self.movex < 0:
            self.left = True
            self.image = pygame.transform.flip(
                self.images[self.frame // ANI], True, False
            )
        else:
            self.attack()
        super().update()
        self.gravity()
        self.hit_ground(grounds)
        self.hit_golem(golems)
        self.hit_iceball(iceballs)
