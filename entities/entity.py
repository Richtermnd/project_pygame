from settings import *

import math
import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, targets, level):
        super().__init__(*groups)
        self.draw_priority = 1
        self.level = level
        self.targets = targets
        self.direction = pygame.math.Vector2()
        self.stats = {}
        self.rotate_angle = math.pi / 2

    def animation(self):
        if self.direction.magnitude() != 0:
            self.cur_sprite = (self.cur_sprite + self.anim_speed) % len(self.sprites)
        image = self.sprites[int(self.cur_sprite)]
        if 90 < math.degrees(self.rotate_angle) < 180 or -180 < math.degrees(self.rotate_angle) < -90:
            image = pygame.transform.flip(image, True, False)
        self.image = image

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.stats['speed']
        self.collision('hor')

        self.hitbox.y += self.direction.y * self.stats['speed']
        self.collision('vert')

        self.rect.center = self.hitbox.center

    def update(self):
        pass

    def collision(self, direction):
        if direction == 'hor':
            for sprite in self.level.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    return True
            return False
        if direction == 'vert':
            for sprite in self.level.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    return True
            return False

    @property
    def pos(self):
        return pygame.math.Vector2(self.rect.center)

    @property
    def level_pos(self):
        x, y = self.pos
        return int(x // TILESIZE), int(y // TILESIZE)

    @property
    def rotate_angle_vector(self):
        return pygame.Vector2(math.cos(self.rotate_angle), math.sin(self.rotate_angle))

    def set_pos(self, topleft):
        x, y = topleft
        self.rect.topleft = x + (TILESIZE - self.rect.w) // 2, y + (TILESIZE - self.rect.w) // 2
        self.hitbox.center = self.rect.center
