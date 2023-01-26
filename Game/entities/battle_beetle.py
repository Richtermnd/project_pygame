from Game.settings import *
import os
from utils import load_image
import pygame
from .base_enemy import BaseEnemy


class BattleBeetle(BaseEnemy):
    __sprites = [load_image(f'enemies/battle_beetle/{image}')
                 for image in os.listdir(r'../sprite_images/enemies/battle_beetle')]
    _death_sound = pygame.mixer.Sound('sounds/enemy_death_sound.ogg')
    stats = {'max hp': 20, 'speed': 8, 'vision': 10, 'damage': 2}

    def __init__(self, *args, **kwargs):
        self.sprites = BattleBeetle.__sprites
        self.death_sound = BattleBeetle._death_sound
        super().__init__(*args, **kwargs)
        self.hitbox = self.rect.inflate(-20, -20)
        self.anim_speed = 5 / FPS

    def update(self):
        super().update()
        if self.hitbox.colliderect(self.target.hitbox):
            self.deal_damage(self.stats['damage'])
