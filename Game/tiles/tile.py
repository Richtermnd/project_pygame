from Game.settings import *
import os

from utils import load_image
import pygame


class Tile(pygame.sprite.Sprite):
    _images = {image: load_image(f'tiles\\walls\\{image}')
               for image in os.listdir(r'..\sprite_images\tiles\walls')}

    def __init__(self, groups: tuple, topleft: tuple):
        super().__init__(*groups)
        self.rect = pygame.Rect(topleft, (TILESIZE, TILESIZE))
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
