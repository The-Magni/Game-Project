import pygame
from character import Character
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ANI = 4
TOTAL_FRAMES = 8 * ANI
ANI_ATCK = 2
TOTAL_FRAMES_ATCK = 8 * ANI_ATCK


class Knight(Character):
    def __init__(self, max_health, xloc, yloc):
        super().__init__(max_health)
        for i in range(1, 9):
            img = pygame.image.load(
                os.path.join("images", "hero_run_" + str(i) + ".png")
            )
            img = pygame.transform.scale_by(img, 0.14)
            img.convert_alpha()
            self.images.append(img)
        
        for i in range(1, 9):
            img = pygame.image.load(
                os.path.join("images", "hero_attack_" + str(i) + ".png")
            )
            img = pygame.transform.scale_by(img, 0.14)
            img.convert_alpha()
            self.attack_images.append(img)

        self.image = pygame.transform.flip(self.images[0], True, False)
        self.rect = self.image.get_bounding_rect()
        self.rect.x = xloc
        self.rect.y = yloc
        self.mask = pygame.mask.from_surface(self.image)

        self.frame = 0
        self.attack_frame = 0
        self.attack_range = pygame.rect.Rect((0, 0, 0, 0))

    def jump(self):
        if not self.is_jumping:
            self.is_falling = False
            self.is_jumping = True

        if self.is_jumping and not self.is_falling:
            self.is_falling = True
            self.movey -= 25

    def hit_golem(self, golems):
        for golem in golems:
            if self.mask.overlap(
                golem.mask, (golem.rect.x - self.rect.x, golem.rect.y - self.rect.y)
            ):
                self.health -= 1

    def attack(self):
        if self.is_attacking:
            if self.attack_frame >= TOTAL_FRAMES_ATCK:
                self.attack_frame = 0
                self.is_attacking = False
            if not self.left:
                self.image = pygame.transform.flip(
                    self.attack_images[self.attack_frame // ANI_ATCK], True, False
                )
            else:
                self.image = self.attack_images[self.attack_frame // ANI_ATCK]
            self.attack_frame += 1

    def update(self, grounds, golems, iceballs):
        if self.movex != 0:
            self.is_jumping = True
            self.frame += 1
        if self.frame >= TOTAL_FRAMES:
            self.frame = 0

        if self.left:
            self.attack_range = pygame.rect.Rect((self.rect.x, self.rect.y), (self.rect.width / 3, self.rect.height))
        else:
            self.attack_range = pygame.rect.Rect((self.rect.centerx + 2 * self.rect.width / 3, self.rect.y), (self.rect.width / 2, self.rect.height),)

        if self.movex < 0:  # canot use else because what about self.movex = 0
            self.image = self.images[self.frame // ANI]
            self.left = True
        elif self.movex > 0:
            self.image = pygame.transform.flip(
                self.images[self.frame // ANI], True, False
            )
            self.left = False
        else:
            if self.left:
                self.image = self.images[0]
            else:
                self.image = pygame.transform.flip(self.images[0], True, False)

        super().update()
        self.gravity()
        self.attack()
        self.hit_ground(grounds)
        self.hit_golem(golems)
        self.hit_iceball(iceballs)
