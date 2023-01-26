import pygame.mixer

from .base_weapon import BaseWeapon
from Game.projectiles import Bullet
from utils import load_image


class Rifle(BaseWeapon):
    _image = load_image(r'weapons/rifle.png')
    _sound = pygame.mixer.Sound('sounds/shoot_sound.mp3')
    _sound.set_volume(0.1)

    def __init__(self, *args, **kwargs):
        self.default_image = Rifle._image
        self.sound = Rifle._sound
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.projectile = Bullet
        self.stats = {'shoots per second': 3}
        super().__init__(*args, **kwargs)
