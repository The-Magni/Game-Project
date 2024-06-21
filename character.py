import pygame
from icecube import Icecube


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ANI = 4
TOTAL_FRAMES = 3 * ANI


class Character(pygame.sprite.Sprite):
    def __init__(self, max_health):
        super().__init__()
        self.left = False
        self.movex = 0
        self.movey = 0
        self.max_health = max_health
        self.health = max_health

        self.is_jumping = True
        self.is_falling = False
        self.is_attacking = False

        self.images = []
        self.attack_images = []
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.freeze_time = 10
        self.is_freeze = False
        self.is_attacked_by_sword = False

    def gravity(self):
        if self.is_jumping:
            self.movey += 3.2

    def hit_ground(self, grounds):
        for ground in grounds:
            if self.mask.overlap(
                ground.mask, (ground.rect.x - self.rect.x, ground.rect.y - self.rect.y)
            ) and (-self.rect.top + ground.rect.bottom >= 0.45 * self.rect.height):
                self.movey = 0
                self.rect.bottom = ground.rect.top
                self.is_jumping = False

    def hit_iceball(self, iceballs):
        for iceball in pygame.sprite.spritecollide(
            self, iceballs, dokill=True, collided=pygame.sprite.collide_mask
        ):
            if not iceball.is_reflected:
                self.health -= 1
                if iceball.can_freeze:
                    self.freeze_time = 10
                    if self.freeze_time:
                        self.freeze_time -= 1
                        self.movex = 0
                        self.is_freeze = True

    def hit_knight(self, knight):
        if knight.is_attacking and self.rect.colliderect(knight.attack_range):
            if not self.is_attacked_by_sword:
                self.health -= 5
                self.is_attacked_by_sword = True
        elif not knight.is_attacking:
            self.is_attacked_by_sword = False

    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom <= 0:
            self.rect.bottom = 0
        if self.rect.top >= SCREEN_HEIGHT:
            self.rect.top = SCREEN_HEIGHT

        if self.left:
            pos = self.rect.bottomright
            self.rect = self.image.get_bounding_rect()
            self.rect.bottomright = pos
            self.mask = pygame.mask.from_surface(self.image)
        else:
            pos = self.rect.bottomleft
            self.rect = self.image.get_bounding_rect()
            self.rect.bottomleft = pos
            self.mask = pygame.mask.from_surface(self.image)

        if self.health <= 0:
            self.rect = pygame.Rect(0, 0, -10000, -10000)
            self.kill()
