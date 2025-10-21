import pygame
from settings import *
from spruits import *
from souuuuuuuundz import *

class Mario:
    def __init__(self, x, y, w, h, sp, jump_pow=27, hp=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = sp
        self.jump_power = jump_pow
        self.hp = hp
        self.SHP = hp
        self.vel_y = 1
        self.alive = True
        self.on_ground = False
        self.disc = 0
        self.dir = 1
        self.animcountr = 0
        self.is_crouching = False

    def move(self):
        self.rect.y += self.vel_y
        self.vel_y += Gr


        if self.rect.top > H:
            self.rect.bottom = 0
            self.rect.x = 100
            self.oooowch(12)
            oof.play()


        if self.vel_y > 20:
            self.vel_y = 20


        if self.disc == 0:


            key = pygame.key.get_pressed()

            if key[pygame.K_RIGHT] and self.rect.right < W:
                self.rect.x += self.speed
                self.dir = 1
                self.is_crouching = False


            elif key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
                self.dir = -1
                self.is_crouching = False
            else:
                self.animcountr = 0

            if key[pygame.K_UP] and self.on_ground:
                if not self.is_crouching:
                    player_jump.play()
                elif self.is_crouching:
                    player_jump_h.play()
                self.vel_y = -self.jump_power
                self.on_ground = False

            if self.on_ground:
                self.speed = 7
            else:
                self.speed = 10
            if key[pygame.K_DOWN] and self.on_ground:
                self.is_crouching = True
                self.jump_power = 35
            if not key[pygame.K_DOWN] and not self.on_ground:
                self.is_crouching = False
                self.jump_power = 27
        else:
            self.rect.x += self.disc
            self.disc -= self.disc // abs(self.disc)


    def oooowch(self, dmg):
        if self.is_crouching:
            self.hp -= dmg // 8
        else:
            self.hp -= dmg
        if self.hp < 1 and self.alive:
            self.alive = False
            self.is_crouching = True
            battle1.stop()
            ded.play()




    def anim(self, sc):
        self.animcountr += 0.4
        if self.animcountr > 98:
            self.animcountr = 0

        sprite_index = int(self.animcountr) % 3

        if self.dir == 1 and self.on_ground and self.alive and not self.is_crouching:
            sc.blit(mario_r_wlk[sprite_index], (self.rect.x, self.rect.y - 7))
        if self.dir == -1 and self.on_ground and self.alive and not self.is_crouching:
            sc.blit(mario_l_wlk[sprite_index], (self.rect.x, self.rect.y - 7))
        if self.dir == 1 and not self.on_ground and self.vel_y < 0 and self.alive and not self.is_crouching:
            sc.blit(mario_r_jump, (self.rect.x, self.rect.y))
        if self.dir == -1 and not self.on_ground and self.vel_y < 0 and self.alive and not self.is_crouching:
            sc.blit(mario_l_jump, (self.rect.x, self.rect.y))
        if self.dir == 1 and not self.on_ground and self.vel_y > 0 and self.alive and not self.is_crouching:
            sc.blit(mario_r_fall, (self.rect.x, self.rect.y))
        if self.dir == -1 and not self.on_ground and self.vel_y > 0 and self.alive and not self.is_crouching:
            sc.blit(mario_l_fall, (self.rect.x, self.rect.y))
        if self.is_crouching and not self.on_ground and self.alive:
            sc.blit(mario_cro_jump, (self.rect.x, self.rect.y))
        if self.is_crouching and self.on_ground and self.alive:
            sc.blit(mario_crouch, (self.rect.x, self.rect.y))
        if not self.alive:
            sc.blit(mario_ouuch, (self.rect.x, self.rect.y + 10))