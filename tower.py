import pygame
from pygame.locals import *
import os
import sys
import globs
import math
import enemy
import itertools
import random


class electric_tower(pygame.sprite.Sprite): # class for the electric tower 
    def __init__(self, pos, hitbox):
        pygame.sprite.Sprite.__init__(self) 
        self.level = 0
        self.image = globs.ELECTRIC_SPRITE
        self.rect = self.image.get_rect(center=pos)
        self.range = 100
        self.x, self.y = pos
        self.damage = 100
        self.cooldown_time = 30
        self.cooldown = self.cooldown_time
        self.lines = []
        self.hitbox = hitbox

    def in_range(self, enemy): #  check if enemy is in range
        if math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) <= self.range:
            return True
        return False

    def line_rendering(self, line): # draw line to enemy, remove before shooting again
        if pygame.time.get_ticks() - line[1] < (self.cooldown_time / 60 * 1000):
            return True
        return False

    def get_target(self, enemies): # get optimal target
        return next(filter(self.in_range, enemies), None)

    def update_lines(self): # remove lines that shouldnt exist anymore
        self.lines = [i for i in self.lines if self.line_rendering(i)]
        for line in self.lines:
            pygame.draw.line(globs.SCREEN, (255, 215, 0), (self.x, self.y), line[0], 3)

    def update(self, e): # main update function
        globs.SCREEN.blit(self.image, (self.x - 16, self.y - 11))
        pygame.draw.circle(globs.SCREEN, (0, 0, 255), (self.x, self.y), self.range, 1)
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.cooldown <= 0 and self.get_target(e):
            target = self.get_target(e)
            self.cooldown = self.cooldown_time
            target.take_damage(self.damage)
            stime = pygame.time.get_ticks()
            self.lines.append([(target.x, target.y), stime])
        self.update_lines()

    def level_up(self): # upgrade
        globs.clicked = True
        globs.player_cash -= 100
        self.level += 1
        self.cooldown -= 5
        self.range += 10
        self.damage += 125


class ice_tower(pygame.sprite.Sprite): # class for the ice tower 
    def __init__(self, pos, hitbox):
        pygame.sprite.Sprite.__init__(self)
        self.level = 0
        self.image = globs.ICE_SPRITE
        self.rect = self.image.get_rect(center=pos)
        self.range = 80
        self.x, self.y = pos
        self.intensity = 0
        self.cycle = itertools.cycle(range(self.intensity + 2))
        self.hitbox = hitbox

    def in_range(self, enemy): # check if in range
        if math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) <= self.range:
            return True
        return False

    def get_targets(self, enemies): # get all targets
        return next(filter(self.in_range, enemies[::-1]), None)

    def update(self, e): # main update function
        globs.SCREEN.blit(self.image, (self.x - 16, self.y - 11))
        pygame.draw.circle(globs.SCREEN, (0, 0, 255), (self.x, self.y), self.range, 1)
        nextcycle = next(self.cycle)
        for enemy in e:
            if self.in_range(enemy):
                globs.SCREEN.blit(globs.cold, (enemy.x - 16, enemy.y - 16))
                enemy.slow = nextcycle

    def level_up(self): # upgrade
        globs.clicked = True
        globs.player_cash -= 100
        self.level += 1
        self.range += 5
        if self.level % 2 == 0:
            self.intensity += 1
            self.cycle = itertools.cycle(range(self.intensity + 2))


class fire_tower(pygame.sprite.Sprite): # class for the fire tower 
    def __init__(self, pos, hitbox):
        pygame.sprite.Sprite.__init__(self)
        self.level = 0
        self.image = globs.FIRE_SPRITE
        self.rect = self.image.get_rect(center=pos)
        self.range = 60
        self.x, self.y = pos
        self.targets = 4
        self.damage = 2
        self.hitbox = hitbox

    def in_range(self, enemy): # get enemies in range
        if math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) <= self.range:
            return True
        return False

    def get_targets(self, enemies): # get optimal targets
        return list(filter(self.in_range, enemies[::-1]))

    def update(self, e): # main update function
        targs = self.get_targets(e)
        globs.SCREEN.blit(self.image, (self.x - 16, self.y - 11))
        pygame.draw.circle(globs.SCREEN, (0, 0, 255), (self.x, self.y), self.range, 1)
        for enemy in targs[: min(self.targets, len(targs))]:
            if self.in_range(enemy):
                pygame.draw.line(
                    globs.SCREEN, (215, 0, 64), (self.x, self.y), (enemy.x, enemy.y), 3
                )
                enemy.take_damage(self.damage)

    def level_up(self): # upgrade
        globs.clicked = True
        globs.player_cash -= 100
        self.level += 1
        self.range += 10
        self.targets += 1
        if self.level % 2 == 0:
            self.damage += 1
