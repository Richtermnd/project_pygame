from ..settings import *
import math
import pygame


class BaseProjectile(pygame.sprite.Sprite):
    def __init__(self, groups, holder, pos):
        super().__init__(*groups)
        self.draw_priority = 0
        self.rect = self.image.get_rect().inflate(-10, -10)

        self.shoot_time = pygame.time.get_ticks()
        self.angle = holder.rotate_angle
        self.direction = holder.rotate_angle_vector
        self.rect.center = self.direction * 40 + pos
        self.start_pos = pygame.Vector2(self.rect.center)
        self.rotate()

    def rotate(self):
        angle = math.degrees(self.angle)
        image = self.image
        if 90 < angle < 180 or -180 < angle < -90:
            image = pygame.transform.flip(image, False, True)
        self.image = pygame.transform.rotate(image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center).inflate(-10, -10)

    def move(self):
        self.rect.center += self.direction * self.shoot_speed

    def fall(self):
        if (pygame.Vector2(self.rect.center) - self.start_pos).length() > self.range:
            self.kill()

    def update(self):
        self.fall()
        self.move()

    @property
    def damage(self):
        return self.stats['damage']

    @property
    def shoot_speed(self):
        return self.stats['tiles_per_second'] * TILESIZE / FPS

    @property
    def is_piercing(self):
        return self.stats['is_piercing']

    @property
    def is_spectral(self):
        return self.stats['is_spectral']

    @property
    def range(self):
        return self.stats['range'] * TILESIZE
