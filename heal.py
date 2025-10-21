import pygame
from settings import *
from souuuuuuuundz import *
class Heal:
    intses = []

    def __init__(self, x, y, targ, targ2, heal=50, vel_y=10):
        self.intses.append(self)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.heal = heal
        self.vel_y = vel_y
        self.targ = targ
        self.targ2 = targ2
    def move(self, plats):
        self.rect.y += self.vel_y
        self.vel_y += Gr / 4
        for plat in plats:
            if self.rect.colliderect(plat):
                self.vel_y = -self.vel_y / 1.2

        if self.rect.colliderect(self.targ):
            self.targ.hp += self.heal
            heal.play()
            if self.targ.hp > self.targ.SHP:
                self.targ.hp = self.targ.SHP
            self.intses.remove(self)
        if self.rect.colliderect(self.targ2):
            self.targ2.hp += self.heal // 3
            heal.play()
            if self.targ2.hp > self.targ2.SHP:
                self.targ2.hp = self.targ2.SHP
            self.intses.remove(self)

        if self.rect.top > H:
            self.intses.remove(self)
