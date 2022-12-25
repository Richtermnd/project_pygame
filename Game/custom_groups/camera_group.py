from Game.settings import *
import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface

    def draw(self, player):
        offset = player.rect.center - CENTER
        for sprite in sorted(self.sprites(), key=lambda x: (-x.draw_priority, x.rect.centery)):
            offset_rect = sprite.rect.topleft - offset
            self.surface.blit(sprite.image, offset_rect)
