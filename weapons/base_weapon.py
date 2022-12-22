from settings import *
import math
import pygame


class BaseWeapon(pygame.sprite.Sprite):
    def __init__(self, holder):
        super().__init__(holder.level.all_sprites, holder.level.visible_sprites)
        self.holder = holder
        self.last_shot = 0
        if self.holder in self.holder.level.players_group:
            self.projectile_group = self.holder.level.player_projectile_sprites
        else:
            self.projectile_group = self.holder.level.enemy_projectile_sprites
        self.projectile_groups = [self.holder.level.all_sprites,
                                  self.holder.level.visible_sprites,
                                  self.projectile_group]

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot >= self.atk_speed:
            self.projectile(self.projectile_groups, self, self.holder.rotate_angle, self.holder.pos)
            self.last_shot = pygame.time.get_ticks()

    def rotate(self):
        angle = math.degrees(self.holder.rotate_angle)
        image = self.default_image
        if 90 < angle < 180 or -180 < angle < -90:
            image = pygame.transform.flip(image, False, True)
        self.image = pygame.transform.rotate(image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update_pos(self):
        self.rect.center = self.holder.rect.center

    def update(self):
        self.rotate()
        self.update_pos()

    @property
    def atk_speed(self):
        return 1000 / self.stats['shoots per second']


