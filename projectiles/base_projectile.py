from settings import *
from utils import angle_vector
import pygame


class BaseProjectile(pygame.sprite.Sprite):
    def __init__(self, groups, weapon, angle, pos):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = self.image.get_masks()

        self.weapon = weapon
        self.shoot_time = pygame.time.get_ticks()
        self.angle = angle
        self.direction = angle_vector(angle)
        self.rotate()

    def rotate(self):
        angle = math.degrees(self.angle)
        image = self.image
        if 90 < angle < 180 or -180 < angle < -90:
            image = pygame.transform.flip(image, False, True)
        self.image = pygame.transform.rotate(image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        self.rect.center += self.direction * self.shoot_speed

    def fall(self):
        if pygame.time.get_ticks() - self.shoot_time > self.fly_time:
            print(pygame.time.get_ticks() - self.shoot_time)
            self.kill()

    def update(self):
        self.fall()
        self.move()

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

    @property
    def fly_time(self):
        return self.shoot_speed * self.range
