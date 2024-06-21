import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img, scale):
        super().__init__()
        img = pygame.image.load(img)
        width = img.get_width()
        height = img.get_height()
        self.image = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def update(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked: #[0] is left clicked
                self.clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False