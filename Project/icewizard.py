import pygame
import math
from wizard import Wizard
from character import Character

ANI = 4
TOTAL_FRAMES = 4 * ANI


class IceWizard(Wizard):
    def __init__(self, max_health, img):
        super().__init__(max_health, img)
        self.attack_range = 350
        self.run_range = 200
        self.rect.center = (650, 0)
        self.is_attacking = False
        self.throw_count = 0

    def hit_fireball(self, fireballs):
        if pygame.sprite.spritecollide(
            self, fireballs, dokill=True, collided=pygame.sprite.collide_mask
        ):
            self.health -= 4

    def distance(self, character):
        return math.sqrt(
            math.pow((self.rect.centerx - character.rect.centerx), 2)
            + math.pow((self.rect.centery - character.rect.centery), 2)
        )

    def attack(self, knight, firewizard):
        if self.distance(knight) > self.run_range:
            if (
                self.distance(knight) <= self.attack_range
                and self.distance(firewizard) <= self.attack_range
            ):
                self.is_attacking = True
                super().attack()
                if not self.is_attacking:
                    self.throw_count = 0
                if self.distance(knight) < self.distance(firewizard):
                    if knight.rect.x < self.rect.x:
                        self.left = True
                    else:
                        self.left = False
                else:
                    if firewizard.rect.x < self.rect.x:
                        self.left = True
                    else:
                        self.left = False
            elif self.distance(knight) <= self.attack_range:
                self.is_attacking = True
                super().attack()
                if not self.is_attacking:
                    self.throw_count = 0
                if knight.rect.x < self.rect.x:
                    self.left = True
                else:
                    self.left = False
            elif self.distance(firewizard) <= self.attack_range:
                self.is_attacking = True
                super().attack()
                if not self.is_attacking:
                    self.throw_count = 0
                if firewizard.rect.x < self.rect.x:
                    self.left = True
                else:
                    self.left = False
            else:
                if not self.left:
                    self.image = self.attack_images[0]
                else:
                    self.image = pygame.transform.flip(
                        self.attack_images[0], True, False
                    )
                self.is_attacking = False

    def move(self, knight):
        if self.distance(knight) <= self.run_range:
            self.is_attacking = False
            if self.rect.x < knight.rect.x:
                self.movex = -2.5
            else:
                self.movex = 2.5
        else:
            self.movex = 0

    def update(self, fireballs, grounds, knight, firewizard):
        Character.update(self)
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
            self.attack(knight, firewizard)

        self.hit_fireball(fireballs)
        self.hit_ground(grounds)
        self.move(knight)
        self.gravity()
        self.hit_knight(knight)
