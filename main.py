import pygame
import random
from settings import *
from maarioo import Mario
from boss import *
from platz import *
from heal import Heal
from spruits import *
from souuuuuuuundz import *
from pygame import gfxdraw

pygame.init()  # Initialize pygame
alpha = 0
fade = 1
win = False
sc = pygame.display.set_mode([W, H])  # create a window
clk = pygame.time.Clock()

healtim = 10 * FPS
player = Mario(100, 100, 50, 50, 7)
boss = Boss(500, -10000, 200, 200, 5, 12, 1, 20, targ=player)

Heal(0, 1000, player, boss)


def draw():
    global alpha
    sc.fill(sky)

    # pygame.draw.rect(sc, (225, 0, 0), player.rect)

    # pygame.draw.rect(sc, (225, 9, 0), boss.rect)
    boss.anim(sc)
    hx = boss.rect.centerx - boss.SHP // 2
    hy = boss.rect.y - 75
    pygame.draw.rect(sc, (0, 0, 0), (hx, hy, boss.SHP, 25))

    if boss.stun:
        pygame.draw.rect(sc, (50, 50, 50), (hx, hy, boss.hp, 25))
    else:
        pygame.draw.rect(sc, (225, 9, 0), (hx, hy, boss.hp, 25))
    pygame.draw.rect(sc, (0, 0, 0), (hx, hy, boss.SHP, 25), 2)

    phx = player.rect.centerx - player.SHP // 2
    phy = player.rect.y - 75

    pygame.draw.rect(sc, (255, 0, 0), (phx, phy, player.SHP, 25))
    pygame.draw.rect(sc, (0, 255, 25), (phx, phy, player.hp, 25))
    pygame.draw.rect(sc, (0, 0, 0), (phx, phy, player.SHP, 25), 2)

    if not player.alive:
        display_text(f'GAME OVER. ', -5, -50, 500)
        player.speed = 0
        player.jump_power = 0


    elif player.rect.y > H:
        display_text(f'GAME OVER. ', -5, 0, 500)
        player.speed = 0
        player.jump_power = 0
        player.hp = 0

    elif player.alive and boss.hp <= 0:
        player.hp = player.SHP
        boss.hp = 0
        battle1.stop()
    elif boss.rect.y > (H + 3500):
        player.hp = player.SHP
        boss.hp = 0
        battle1.stop()

    for heal in Heal.intses:
        heal.move(plats)
        sc.blit(super_heart, (heal.rect.x, heal.rect.y))


def display_text(text, x, y, size):
    font = pygame.font.Font('Fixedsys.ttf', size)
    render = font.render(text, True, (200, 50, 50))
    sc.blit(render, (x, y))


battle1.play(-1)

while True:

    draw()
    player.move()
    boss.move()

    healtim -= 1
    if healtim <= 0:
        healtim = 10 * FPS
        Heal(random.randint(10, W - 40), -50, player, boss)
    if player.rect.colliderect(boss):
        right = abs(player.rect.right - boss.rect.left)
        left = abs(player.rect.left - boss.rect.right)
        top = abs(player.rect.top - boss.rect.bottom)
        bottom = abs(player.rect.bottom - boss.rect.top)
        if bottom < col_tolr:
            player.vel_y = -20
            if boss.stun:
                player.oooowch(1)
                oof.play()
            else:
                boom.play()
                boss.oooch(random.randint(10, 20))
        elif top < col_tolr:
            oof.play()
            player.oooowch(5)
            if boss.is_alive:
                boss.vel_y = -boss.jpow
        elif right < col_tolr:
            oof.play()
            player.oooowch(8)
            player.rect.right = boss.rect.left
            player.disc = -25
        elif left < col_tolr:
            oof.play()
            player.oooowch(8)
            player.rect.left = boss.rect.right
            player.disc = 25

    for plat in plats:
        pygame.draw.rect(sc, (50, 50, 50), plat)

        if player.rect.colliderect(plat):
            right = abs(player.rect.right - plat.left)
            left = abs(player.rect.left - plat.right)
            top = abs(player.rect.top - plat.bottom)
            bottom = abs(player.rect.bottom - plat.top)

            if bottom < col_tolr:
                player.rect.bottom = plat.top
                player.vel_y = 0
                player.on_ground = True
            elif top < col_tolr:
                player.rect.top = plat.bottom
                player.vel_y = 0
            if right < col_tolr // 3:
                player.disc = 0
                player.rect.right = plat.left
            elif left < col_tolr // 3:
                player.disc = 0
                player.rect.left = plat.right



    if isinstance(boss, Boudergeist) and boss.rect.y >= 2500:
        display_text("You Win!!!",20, 200, 500)

        if not win:
            battle2.fadeout(10)
            win_e.play(-1)
            win = True
    if boss.rect.y > 3000:
        alpha += fade
        player.speed = 0
        if alpha >= 255:
            fade = -1
            plats = [pygame.Rect(0, 1000, W - 600, 200),
                     pygame.Rect(-100, 100, 100, H),
                     pygame.Rect(W, -100, 100, H), ]
            # lvl
        if alpha < 0:
            fade = 1
            alpha = 0
            player.speed = 7
            boss = Boudergeist(W - 375, 550, 300, 400, 4, 200, 99, 0, targ=player)
            battle2.play(-1)

        gfxdraw.box(sc, (0, 0, W, H), (0, 0, 0, int(alpha)))

    player.anim(sc)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    pygame.display.flip()
    clk.tick(FPS)
