from .base_weapon import BaseWeapon
from projectiles import Bullet
from utils import load_image


class Rifle(BaseWeapon):
    __image = load_image(r'weapons\carbine.png')
    # __image = __image.convert_alpha()

    def __init__(self, *args, **kwargs):
        self.default_image = Rifle.__image
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.projectile = Bullet
        self.stats = {'shoots per second': 3}
        super().__init__(*args, **kwargs)
