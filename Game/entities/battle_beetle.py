from Game.settings import *
import os
from utils import load_image
import pygame
from .base_enemy import BaseEnemy


class BattleBeetle(BaseEnemy):
    __sprites = [load_image(f'enemies\\battle_beetle\\{image}')
                 for image in os.listdir(r'..\sprite_images\enemies\battle_beetle')]

    def __init__(self, *args, **kwargs):
        self.sprites = BattleBeetle.__sprites
        self.cur_sprite = 0
        self.anim_speed = 5 / FPS
        self.image = self.sprites[self.cur_sprite]
        self.rect = pygame.Rect(5, 5, self.image.get_size()[0] - 5, self.image.get_size()[1] - 5)
        self.hitbox = self.rect.inflate(-20, -20)
        super().__init__(*args, **kwargs)
        self.stats = {'speed': 2, 'vision': 10}

    def update(self):
        self.move()
        self.anti_stuck()
        self.check_target()
        self.animation()
