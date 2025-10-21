import pygame.transform
import random
from platz import plats
from settings import *
from spruits import *
from souuuuuuuundz import *


class Boss:
    def __init__(self, x, y, w, h, sp, hp, dam, jump_pow, targ):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = sp
        self.hp = hp
        self.SHP = hp
        self.dam = dam
        self.jpow = jump_pow
        self.targ = targ
        self.vel_y = 0
        self.dir = 0
        self.on_ground = True
        self.stun = False
        self.stun_count = 0
        self.anim_count = 0
        self.is_alive = True

    def move(self):

        self.chase()
        if self.stun:
            self.stun_count -= 1
            if self.stun_count <= 0:
                self.stun = False

        self.rect.y += self.vel_y
        self.vel_y += Gr
        if self.vel_y > 20:
            self.vel_y = 20
        if self.hp < 1 and self.is_alive:
            self.speed = 0
            self.is_alive = False
            self.jump()

            pygame.mixer.music.load('1-10. You Got a Moon! 1.mp3')

            pygame.mixer.music.play()

        if self.is_alive:
            for plat in plats:

                if self.rect.colliderect(plat):
                    right = abs(self.rect.right - plat.left)
                    left = abs(self.rect.left - plat.right)
                    top = abs(self.rect.top - plat.bottom)
                    bottom = abs(self.rect.bottom - plat.top)

                    col_tolr = 100

                    if bottom < col_tolr:
                        self.rect.bottom = plat.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif top < col_tolr:
                        self.rect.top = plat.bottom
                        self.vel_y = 0
                    if right < col_tolr // 4:
                        if plat.h > 500:
                            self.dir = -self.dir
                        self.rect.right = plat.left
                        self.jump()
                    elif left < col_tolr // 4:
                        if plat.h > 500:
                            self.dir = -self.dir
                        self.rect.left = plat.right
                        self.jump()

    def chase(self):
        dist = abs(self.targ.rect.centerx - self.rect.centerx + 0.00000001)
        if self.stun:
            self.dir = -(self.targ.rect.centerx - self.rect.centerx) / dist
            self.dir *= 3.5
        elif dist > 200:
            self.dir = (self.targ.rect.centerx - self.rect.centerx) / dist
        self.rect.x += self.dir * self.speed


    def oooch(self, dam):
        if not self.stun:
            self.hp -= dam
            self.vel_y -= 5
            self.stun = True
            self.stun_count = 200

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.vel_y = -self.jpow

    def anim(self, sc):
        self.anim_count += 0.1
        if self.anim_count > 99:
            self.anim_count = 0

        sprite_index_b = int(self.anim_count) % 2
        if self.on_ground and not self.stun and self.is_alive:
            sc.blit(boomwlk[sprite_index_b], (self.rect.x, self.rect.y))
        if not self.on_ground and not self.stun and self.is_alive:
            if self.vel_y < 0 and self.is_alive:
                sc.blit(boom_idle, (self.rect.x, self.rect.y))
            if self.vel_y > 0 and self.is_alive:
                sc.blit(boom_jump, (self.rect.x, self.rect.y))
                pow.play()
        if self.stun and self.is_alive:
            if self.stun_count > 120 and self.is_alive:
                sc.blit(boom_oouch, (self.rect.x, self.rect.y + 140))
            else:
                if self.on_ground and self.is_alive:
                    sc.blit(boom_block_fall, (self.rect.x, self.rect.y + 70))
                elif self.vel_y < 0 and self.is_alive:
                    sc.blit(boom_block_jump, (self.rect.x, self.rect.y + 70))
                else:
                    sc.blit(boom_block_fall, (self.rect.x, self.rect.y + 70))
        if not self.is_alive:
            sc.blit(boomdead[int(self.anim_count) % 2], (self.rect.x, self.rect.y))
            self.stun_count = 0


class Boudergeist:
    def __init__(self, x, y, w, h, sp, hp, dam, jump_pow, targ):
        self.rect = pygame.Rect(W, y, w, h)
        self.anim_x = x
        self.speed = sp
        self.hp = hp
        self.SHP = hp
        self.dam = dam
        self.jpow = jump_pow
        self.targ = targ
        self.vel_y = 0
        self.dir = 0
        self.on_ground = True
        self.stun = False
        self.stun_count = 0
        self.anim_count = 0
        self.is_alive = True
        self.just_spawned = True
        self.attack_coutr = 0

    def move(self):
        self.attack_coutr += 1
        if self.attack_coutr > 80 and self.hp > 0:
            Rock(self.rect.x, self.rect.y, self.targ.rect.center, 15)

            self.attack_coutr = 0

        if self.just_spawned:
            delta = (self.anim_x - self.rect.x) // 239
            self.rect.x += delta

        if self.hp <= 0:
            self.hp = -100
            self.rect.x += random.uniform(-5,5)
            self.rect.y += random.uniform(-1,1)
            if self.attack_coutr > 300:
                self.vel_y += Gr
                self.rect.y += self.vel_y
            if self.rect.y > 2500:
                self.attack_coutr = 0
                self.vel_y = 0

    def oooch(self, dam):
        self.targ.hp -= dam
        self.targ.vel_y = -self.targ.jump_power
        self.targ.disc = -50

    def anim(self, sc):
        self.anim_count += 0.1
        if self.anim_count > 98:
            self.anim_count = 0

        sprite_index_bo = int(self.anim_count) % 2
        if not self.stun and self.is_alive:
            sc.blit(bould_idle[sprite_index_bo], (self.rect.x, self.rect.y))
        if self.stun:
            sc.blit(bould_ouch, (self.rect.x, self.rect.y))
            self.stun_count -= 1
            if self.stun_count < 0:
                self.stun = False

        if self.hp < 0:
            sc.blit(bould_dead[sprite_index_bo], (self.rect.x, self.rect.y))


        elif self.hp < self.SHP: #// 2
            if len(Spike.instanses) == 0:
                Spike(self.rect.x - 100, H + 100, self.targ, 10)
                Spike(self.rect.x - 110, H + 2000, self.targ, 11)
                Spike(self.rect.x - 100, H + 100, self.targ, 12)
                Spike(self.rect.x - 110, H + 2000, self.targ, 13)
                Spike(self.rect.x - 110, H + 2000, self.targ, 14)
            for spike in Spike.instanses:
                spike.move()
                spike.anim(sc)
                if self.targ.rect.colliderect(spike.rect):
                    self.targ.oooowch(0.7)


        for rock in Rock.intstanses:
            rock.move()
            rock.anim(sc)
            if self.targ.rect.colliderect(rock.rect):
                if not rock.cracked and not rock.broken and self.targ.vel_y < 0:
                    self.targ.vel_y = 0
                    rock.cracked = True
                    rock.center_y = -rock.speed
                    rock.going_back = True

                elif not rock.broken and rock.center_y > 0:
                    self.targ.oooowch(15)
                    rock.broken = True
                    rock.cracked = False
                    rock.center_y /= 2
            if rock.rect.colliderect(plats[0]):
                rock.broken = True
                rock.cracked = False
            if rock.rect.colliderect(self.rect) and rock.going_back and not rock.broken:
                rock.broken = True
                rock.cracked = False
                rock.center_y /= 2
                self.hp -= 29
                self.stun = True
                self.stun_count = 5


class Rock:
    intstanses = []

    def __init__(self, x, y, targ, speed, size=150):
        self.intstanses.append(self)
        self.bouldergeist = (x, y)
        self.rect = pygame.Rect(x, y, size, size)
        self.targ = targ
        self.speed = speed
        self.size = size
        self.cracked = random.choice([False, False, True, True, True])
        self.broken = False
        self.center_x = 0
        self.center_y = -speed
        self.going_back = False

    def move(self):
        self.rect.x += self.center_x
        self.rect.y += self.center_y
        if self.rect.bottom < 0 and not self.going_back:
            self.center_y = self.speed
            self.rect.x = self.targ[0]
            self.rect.y = -150
        if self.rect.top > H:
            self.intstanses.remove(self)

        if self.rect.bottom < 0 and self.going_back:
            self.center_y = self.speed
            self.rect.x = self.bouldergeist[0]
            self.rect.y = -20


    def anim(self, sc):
        if not self.cracked and not self.broken:
            sc.blit(rock_whole, (self.rect.x, self.rect.y))
        if self.cracked:
            sc.blit(rock_cracked, (self.rect.x, self.rect.y))
        if self.broken:
            sc.blit(rock_broken, (self.rect.x, self.rect.y))


class Spike:
    instanses = []

    def __init__(self, x, y, targ, speed, w=300, h=150):
        self.instanses.append(self)
        self.spawn_x = x
        self.rect = pygame.Rect(x, y, w, h)
        self.targ = targ.rect
        self.sp = speed

        self.attacking = False
        self.attack_count = 200
        self.anim_count = 0
    def move(self):
        if self.attacking:
            self.rect.x -= self.sp
        if not self.attacking:
            self.rect.y += (self.targ.y - self.rect.y) / 15

            self.attack_count -= 1
            if self.attack_count < 0:
                self.attacking = True

        if self.rect.right < 0:
            self.rect.top = H
            self.rect.x = self.spawn_x
            self.attacking = False
            self.attack_count = 200


    def anim(self, sc):
        self.anim_count += 0.1
        if self.anim_count > 98:
            self.anim_count = 0

        sprite_index_s = int(self.anim_count) % 2
        if self.attacking:
            sc.blit(spike_attack[sprite_index_s], (self.rect.x, self.rect.y))
        if not self.attacking:
            sc.blit(spike_idle[sprite_index_s], (self.rect.x, self.rect.y))
