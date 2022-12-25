from Game.settings import *
import math
import pygame
import os

from utils import load_image
from .entity import Entity
from Game.weapons import Rifle


class Player(Entity):
    __sprites = [load_image(f'player\\{image}') for image in os.listdir(r'..\sprite_images\player')]
    __sprites = [pygame.transform.scale(image, (image.get_size()[0] * 1.2, image.get_size()[1] * 1.2))
                 for image in __sprites]

    def __init__(self, *args, **kwargs):
        self.sprites = Player.__sprites
        self.cur_sprite = 0
        self.anim_speed = 12 / FPS  # 12 frame per second
        self.image = self.sprites[self.cur_sprite]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(0, -20)
        super().__init__(*args, **kwargs)

        self.stats = {'speed': 5}
        self.first_weapon = Rifle(self)
        self.second_weapon = None

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_pos_relative = mouse_pos - CENTER + pygame.Vector2(10 ** -3, 10 ** -3)  # position relative to the center

        if keys[pygame.K_s]:
            self.direction.y = 1
        elif keys[pygame.K_w]:
            self.direction.y = -1
        else:
            self.direction.y = 0
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if mouse_buttons[0]:
            self.first_weapon.shoot()

        acos_a = math.acos(mouse_pos_relative.x / mouse_pos_relative.length())
        asin_a = math.asin(mouse_pos_relative.y / mouse_pos_relative.length())

        self.rotate_angle = acos_a * (asin_a // abs(asin_a) if asin_a != 0 else 1)

    def draw_aim(self):
        cos_a, sin_a = self.rotate_angle_vector
        start_pos = CENTER
        end_pos = start_pos + pygame.Vector2(cos_a, sin_a) * CENTER.length()
        pygame.draw.line(self.level, 'red', start_pos, end_pos)

    def update(self):
        self.input()
        self.move()
        self.animation()
        self.draw_aim()
