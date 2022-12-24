from utils import load_image
from .base_projectile import BaseProjectile


class Bullet(BaseProjectile):
    __image = load_image(r'projectiles\bullet.png').convert_alpha()

    def __init__(self, *args, **kwargs):
        self.image = Bullet.__image
        super().__init__(*args, **kwargs)
        self.stats = {'tiles_per_second': 20,
                      'damage': 3,
                      'range': 10,
                      'is_piercing': False,
                      'is_spectral': False}
