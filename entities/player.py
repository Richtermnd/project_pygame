from settings import *
import math
import pygame
import os

from utils import load_image
from .entity import Entity
from weapons import Rifle


class Player(Entity):
    __images = [pygame.transform.scale(load_image(f'player\\{image}'), (TILESIZE - 10, TILESIZE)) for image in os.listdir(r'sprite_images\player')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cur_sprite = 0
        self.image = Player.__images[self.cur_sprite]
        self.rect = self.image.get_rect()
        self.stats = {'speed': 5}
        self.first_weapon = Rifle(self)
        self.second_weapon = None

    def animation(self):
        if self.direction.magnitude() != 0:
            self.cur_sprite = (self.cur_sprite + 0.2) % len(Player.__images)
        image = Player.__images[int(self.cur_sprite)]
        if 90 < math.degrees(self.rotate_angle) < 180 or -180 < math.degrees(self.rotate_angle) < -90:
            image = pygame.transform.flip(image, True, False)
        self.image = image

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

    def collision(self, direction):
        if direction == 'hor':
            if sprite := pygame.sprite.spritecollideany(self, self.level.obstacle_sprites):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
        if direction == 'vert':
            if sprite := pygame.sprite.spritecollideany(self, self.level.obstacle_sprites):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

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
