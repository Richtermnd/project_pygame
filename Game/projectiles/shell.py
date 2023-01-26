from utils import load_image
from .base_projectile import BaseProjectile


class Shell(BaseProjectile):
    __image = load_image(r'projectiles\shell.png').convert_alpha()

    def __init__(self, *args, **kwargs):
        self.image = Shell.__image
        super().__init__(*args, **kwargs)
        self.stats = {'tiles_per_second': 30,
                      'damage': 2,
                      'range': 2,
                      'is_piercing': False,
                      'is_spectral': False}
