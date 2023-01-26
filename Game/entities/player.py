import utils
from Game.settings import *
import math
import pygame
import os

from utils import load_image
from .entity import Entity
from Game.weapons import Rifle, Shotgun


font = pygame.font.Font(None, 40)


class PlayerInterface(pygame.Surface):
    def __init__(self, player):
        super().__init__((250, 100), pygame.SRCALPHA)
        self.player = player
        self.convert_alpha()
        self.hp_bar = pygame.Surface((240, 40), pygame.SRCALPHA)
        self.weapon_block = pygame.Surface((240, 40), pygame.SRCALPHA)

    def draw_hp_bar(self):
        # rect
        self.hp_bar.fill('black')
        pygame.draw.rect(self.hp_bar, 'white', self.hp_bar.get_rect(), 5, border_radius=3)
        w, h = self.hp_bar.get_size()
        rect_w = (w - 10) / self.player.stats['max hp'] * self.player.hp
        pygame.draw.rect(self.hp_bar, 'red', (5, 5, rect_w, 30))

        # text
        text = font.render(f'{self.player.hp}/{self.player.stats["max hp"]}', True, 'white')
        self.hp_bar.blit(text, (w / 2 - text.get_size()[0] / 2, 7))
        self.blit(self.hp_bar, (5, 5))

    def draw_weapon_block(self):
        surf = pygame.Surface((120, 40), pygame.SRCALPHA)
        pygame.draw.rect(surf, 'black', surf.get_rect(), border_radius=3)
        pygame.draw.rect(surf, 'white', surf.get_rect(), 5, border_radius=3)
        pos_x = (surf.get_width() - self.player.first_weapon.default_image.get_width()) / 2
        pos_y = (surf.get_height() - self.player.first_weapon.default_image.get_height()) / 2
        surf.blit(self.player.first_weapon.default_image, (pos_x, pos_y))
        self.weapon_block.blit(surf, (0, 0))

        surf = pygame.Surface((120, 40), pygame.SRCALPHA)
        surf.convert_alpha()
        pygame.draw.rect(surf, 'black', surf.get_rect(), border_radius=3)
        pygame.draw.rect(surf, 'white', surf.get_rect(), 5, border_radius=3)
        pos_x = (surf.get_width() - self.player.second_weapon.default_image.get_width()) / 2
        pos_y = (surf.get_height() - self.player.second_weapon.default_image.get_height()) / 2
        surf.blit(self.player.second_weapon.default_image, (pos_x, pos_y))
        self.weapon_block.blit(surf, (120, 0))
        self.blit(self.weapon_block, (5, 55))

    def draw(self):
        self.draw_hp_bar()
        self.draw_weapon_block()
        self.player.level.blit(self, (0, 0))


class Player(Entity):
    __sprites = [load_image(f'player\\{image}') for image in os.listdir(r'..\sprite_images\player')]
    __sprites = [pygame.transform.scale(image, (image.get_size()[0] * 1.2, image.get_size()[1] * 1.2))
                 for image in __sprites]

    def __init__(self, *args, **kwargs):
        self.last_hit = 0
        self.last_swap = 0
        self.sprites = Player.__sprites
        self.stats = {'max hp': 8, 'speed': 10}
        super().__init__(*args, **kwargs)
        self.anim_speed = 12 / FPS  # 12 frame per second
        self.hitbox = self.rect.inflate(0, -20)

        self.first_weapon = Rifle(self)
        self.first_weapon.is_active = True
        self.second_weapon = Shotgun(self)
        self.interface = PlayerInterface(self)

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

        if keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_swap > 500:
                self.first_weapon, self.second_weapon = self.second_weapon, self.first_weapon
                self.first_weapon.is_active = True
                self.second_weapon.is_active = False
                self.last_swap = pygame.time.get_ticks()

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

    def change_hp(self, change):
        if pygame.time.get_ticks() - self.last_hit > 1000:
            super().change_hp(change)
            if self.hp <= 0:
                self.level.game.running = False
            self.last_hit = pygame.time.get_ticks()

    def update(self):
        super().update()
        self.input()
        self.move()
        self.animation()
        self.draw_aim()
        self.interface.draw()
