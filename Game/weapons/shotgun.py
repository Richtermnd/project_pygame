import pygame.mixer

from .base_weapon import BaseWeapon
from Game.projectiles import Shell
from utils import load_image, angle_to_vector
import math


class Shotgun(BaseWeapon):
    _image = load_image(r'weapons/shotgun.png')
    _sound = pygame.mixer.Sound('sounds/shoot_sound.mp3')
    _sound.set_volume(0.1)

    def __init__(self, *args, **kwargs):
        self.default_image = Shotgun._image
        self.sound = Shotgun._sound
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.projectile = Shell
        self.stats = {'shoots per second': 1}
        super().__init__(*args, **kwargs)

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot >= self.atk_speed:
            self.sound.play()
            for shell in range(-3, 4):
                proj = self.projectile(self.projectile_groups, self.holder, self.holder.pos)
                proj.angle += math.pi / 36 * shell
                proj.direction = angle_to_vector(proj.angle)

            self.last_shot = pygame.time.get_ticks()
