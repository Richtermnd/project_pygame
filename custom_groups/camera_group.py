from settings import *
import pygame
from tiles import _Tile


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface):
        super().__init__()
        self.display_surface = surface

    def draw(self, player):
        offset = player.rect.center - CENTER
        for sprite in sorted(self.sprites(), key=lambda x: not isinstance(x, _Tile)):
            offset_rect = sprite.rect.topleft - offset
            self.display_surface.blit(sprite.image, offset_rect)
