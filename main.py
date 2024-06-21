import pygame
from knight import Knight
from ground import Ground
from health_bar import HealthBar
from wizard import Wizard
from throwable import Throwable
from explosion import Explosion
from icewizard import IceWizard
from iceball import Iceball
from golem import Golem
from icecube import Icecube
from button import Button
import os


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
STEPS = 5
FPS = 30  # frame rate
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
BACKGROUND_COLOR = (190, 190, 190)
INSTRUCTION_TEXT = ["There are 2 players, the Knight and the FireWizard.",
                    "Your plan is to defeat all the enemies.",
                    "- The Knight use the arrows key to move, and spacebar to attack",
                    "- The Firewizard use WAD to move, and S to attack",
                    "There are 2 kinds of enemies, Golem and Icewizard:",
                    "- Icewizard can shoot iceball, there is 50% chance it can freeze your player",
                    "- Golem will chase you if you are too close, you will lose health touching them",
                    ]
THANKS_TEXT = ["Many images I use in this game are created by others. I want to give special thanks to:",
               "- Segel for the knight animation images",
               "- tautomer for the ice golem animation images",
               "- CraftPix.net 2D Game Assets for both wizard animation images",
               "- CRAFTPIC.NET for the explosion animation",
               "- Epcartoonz for the icecube image",
               "- ScagHound for the fireball animation",
               "- Mobile Game Graphics for the iceball animation",
               "The detail licenses can be read at the file README.md."
               ]
FONT = pygame.font.SysFont("Times New Roman", 36)

def play():
    # setting up screen background
    backdrop = pygame.image.load(os.path.join("images", "background.png"))
    backdropbox = SCREEN.get_rect()  # a tuple of size of screen
    # set up clock
    clock = pygame.time.Clock()
    # initialize sprite group
    all_sprites = pygame.sprite.Group()
    icecubes = pygame.sprite.Group()
    players = pygame.sprite.Group()
    fireballs = pygame.sprite.Group()
    golems = pygame.sprite.Group()
    grounds_and_enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    iceballs = pygame.sprite.Group()
    grounds = pygame.sprite.Group()
    # Initialize sprite
    knight = Knight(10, 200, 700)
    firewizard = Wizard(8, "firewizard")
    icewizard = IceWizard(8, "icewizard")
    # Adding sprite to group
    all_sprites.add(knight)
    all_sprites.add(firewizard)
    players.add(knight)
    players.add(firewizard)
    golems.add(Golem(40, 200, 150))
    golems.add(Golem(40, 500, 500))
    all_sprites.add(golems)
    grounds_and_enemies.add(golems)
    all_sprites.add(icewizard)
    grounds_and_enemies.add(icewizard)
    # initailize grounds
    xlocs = [50, 300, 600, 200, 350, 330, 550, 100, 170, 750]
    ylocs = [500, 400, 450, 400, 300, 150, 170, 100, 220, 50]
    main_ground = Ground(-10, 580, 80, 900)
    grounds.add(main_ground)
    for i in range(10):
        ground = Ground(xlocs[i], ylocs[i])
        grounds.add(ground)
    all_sprites.add(grounds)
    grounds_and_enemies.add(grounds)
    # Initialize healthbar
    knight_health_bar = HealthBar(50, 5, knight)
    firewizard_health_bar = HealthBar(40, 5, firewizard)
    golem_health_bars = pygame.sprite.Group()
    for golem in golems:
        golem_health_bars.add(HealthBar(200, 5, golem))
    icewizard_health_bar = HealthBar(40, 5, icewizard)

    # main game loop
    while True:
        # pressing key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    knight.movex = -STEPS
                if event.key == pygame.K_RIGHT:
                    knight.movex = STEPS
                if event.key == pygame.K_SPACE:
                    knight.is_attacking = True
                    knight.attack()
                if event.key == pygame.K_UP:
                    knight.jump()
                if event.key == ord("a"):
                    firewizard.movex = -STEPS / 2
                if event.key == ord("d"):
                    firewizard.movex = STEPS / 2
                if event.key == ord("w"):
                    firewizard.jump()
                if (
                    event.key == ord("s")
                    and not firewizard.is_attacking
                    and firewizard.movex == 0
                ):
                    firewizard.is_attacking = True
                    fireball = Throwable(
                        firewizard.rect.centerx, firewizard.rect.top, "fireball", 3
                    )
                    fireball.left = firewizard.left
                    fireballs.add(fireball)
                    all_sprites.add(fireball)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    knight.movex = 0
                if event.key == pygame.K_RIGHT:
                    knight.movex = 0
                if event.key == ord("a"):
                    firewizard.movex = 0
                    firewizard.left = True
                if event.key == ord("d"):
                    firewizard.movex = 0
                    firewizard.left = False

        if knight.health <= 0 and firewizard.health <= 0:
            main()
            break

        if icewizard.is_attacking and icewizard.throw_count < 1:
            iceball = Iceball(
                icewizard.rect.centerx,
                icewizard.rect.centery,
                "iceball",
                1.5,
                knight,
                firewizard,
            )
            iceballs.add(iceball)
            all_sprites.add(iceball)
            icewizard.throw_count += 1

        for fireball in fireballs:
            if pygame.sprite.spritecollide(
                fireball,
                grounds_and_enemies,
                dokill=False,
                collided=pygame.sprite.collide_mask,
            ):
                explosion = Explosion(fireball.rect.center)
                explosions.add(explosion)
                all_sprites.add(explosion)

        for player in players:
            if player.is_freeze and not any(
                icecube
                for icecube in icecubes
                if icecube.rect.center == player.rect.center
            ):
                icecube = Icecube(player)
                icecubes.add(icecube)
                all_sprites.add(icecube)

        # update the sprite
        golems.update(grounds, knight, firewizard, fireballs)
        knight.update(grounds, golems, iceballs)
        firewizard.update(grounds, golems, iceballs)
        icewizard.update(fireballs, grounds, knight, firewizard)
        explosions.update()
        fireballs.update(SCREEN_WIDTH, SCREEN_HEIGHT, grounds)
        iceballs.update(SCREEN_HEIGHT, SCREEN_WIDTH, knight)
        icecubes.update()
        # update the health bar
        knight_health_bar.update()
        golem_health_bars.update()
        firewizard_health_bar.update()
        icewizard_health_bar.update()

        # Drawing screen
        SCREEN.blit(backdrop, backdropbox)

        # Drawing sprites
        knight_health_bar.appear(SCREEN)
        for golem_health_bar in golem_health_bars:
            golem_health_bar.appear(SCREEN)
        firewizard_health_bar.appear(SCREEN)
        icewizard_health_bar.appear(SCREEN)

        # Drawing characters
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        play_button = Button(SCREEN_WIDTH / 2, 150, "images/play_button.png", 1)
        instruction_button = Button(
            SCREEN_WIDTH / 2, 300, "images/instruction_button.png", 1
        )
        thanks_button = Button(SCREEN_WIDTH / 2, 450, "images/thanks_button.png", 1)
        buttons = pygame.sprite.Group()
        buttons.add(play_button)
        buttons.add(instruction_button)
        buttons.add(thanks_button)
        SCREEN.fill(BACKGROUND_COLOR)
        buttons.draw(SCREEN)
        pygame.display.flip()
        buttons.update()
        if play_button.clicked:
            play()
            break
        elif instruction_button.clicked:
            instruction()
            break
        elif thanks_button.clicked:
            thanks()
            break


def instruction():
    while True:
        SCREEN.fill(BACKGROUND_COLOR)
        back_button = Button(115, SCREEN_HEIGHT - 100, "images/back_button.png", 0.5)
        back_button.update()
        SCREEN.blit(back_button.image, back_button.rect)
        if back_button.clicked:
            main()
            break
        render_multiline_text(INSTRUCTION_TEXT, FONT, (20, 20))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def render_multiline_text(text, font, start_pos):
    x, y = start_pos
    new_text = wrap_text(text, font, SCREEN_WIDTH - 20)
    for line in new_text:
        text_surf = font.render(line, True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.topleft = (x, y)
        SCREEN.blit(text_surf, text_rect)
        y += font.get_linesize()


def wrap_text(text, font, max_width):
    wrapped_lines = []
    current_line = ""

    for line in text:
        words = line.split(" ")
        for word in words:
            test_line = current_line + " " + word
            test_width = font.size(test_line)[0]
            if test_width <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word + " "
        wrapped_lines.append(current_line)
        current_line = ""

    return wrapped_lines


def thanks():
    while True:
        SCREEN.fill(BACKGROUND_COLOR)
        back_button = Button(115, SCREEN_HEIGHT - 50, "images/back_button.png", 0.5)
        back_button.update()
        SCREEN.blit(back_button.image, back_button.rect)
        if back_button.clicked:
            main()
            break
        render_multiline_text(THANKS_TEXT, FONT, (20, 20))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__ == "__main__":
    main()
