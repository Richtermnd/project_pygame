from settings import *

import math
import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, targets, level):
        super().__init__(*groups)
        self.level = level
        self.targets = targets
        self.direction = pygame.math.Vector2()
        self.stats = {}
        self.rotate_angle = math.pi / 2

    def draw_aim(self):
        pass

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.stats['speed']
        self.collision('hor')

        self.rect.y += self.direction.y * self.stats['speed']
        self.collision('vert')

    def update(self):
        pass

    def collision(self, direction):
        if direction == 'hor':
            for sprite in self.level.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == 'vert':
            for sprite in self.level.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    @property
    def pos(self):
        return pygame.math.Vector2(self.rect.center)

    @property
    def level_pos(self):
        x, y = self.pos
        return x // TILESIZE, y // TILESIZE

    @property
    def rotate_angle_vector(self):
        return pygame.Vector2(math.cos(self.rotate_angle), math.sin(self.rotate_angle))

    def set_pos(self, topleft):
        x, y = topleft
        self.rect.topleft = x + (TILESIZE - self.rect.w) // 2, y + (TILESIZE - self.rect.w) // 2