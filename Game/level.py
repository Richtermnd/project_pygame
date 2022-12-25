from Game.settings import *
import pygame
import utils
import custom_groups
from tiles import Floor, Wall
import entities


def load_map(level_file):
    with open(level_file) as level:
        level_map = [list(row.strip()) for row in level.readlines()]
    return level_map


class Level(pygame.Surface):
    def __init__(self, level_file):
        super().__init__(SIZE)
        # -- generalized custom_groups --
        self.all_sprites = pygame.sprite.Group()
        self.visible_sprites = custom_groups.CameraGroup(self)

        # -- level groups --
        self.obstacle_sprites = pygame.sprite.Group()

        # -- entities group --
        self.enemies_group = pygame.sprite.Group()
        self.players_group = pygame.sprite.GroupSingle()
        # -- projectile custom_groups --
        self.player_projectile_sprites = custom_groups.ProjectileGroup(self.enemies_group, self.obstacle_sprites)
        self.enemy_projectile_sprites = custom_groups.ProjectileGroup(self.players_group, self.obstacle_sprites)

        self.screen = pygame.display.get_surface()
        self.player = entities.Player((self.all_sprites, self.players_group, self.visible_sprites),
                                      self.enemies_group, self)
        self.level_map = load_map(level_file)
        self.generate_level()

    def generate_level(self):
        for y, row in enumerate(self.level_map):
            for x, col in enumerate(row):
                topleft = x * TILESIZE, y * TILESIZE
                match col:
                    case '#':
                        Wall((self.all_sprites, self.obstacle_sprites, self.visible_sprites),
                             topleft,
                             utils.tile_neighbors(self.level_map, (x, y)))
                    case '.':
                        Floor((self.all_sprites, self.visible_sprites), topleft)
                    case 'p':
                        self.player.set_pos(topleft)
                        Floor((self.all_sprites, self.visible_sprites), topleft)
                    case 'r':
                        entities.BattleBeetle((self.all_sprites, self.enemies_group, self.visible_sprites),
                                              self.players_group, self).set_pos(topleft)

                        Floor((self.all_sprites, self.visible_sprites), topleft)

    def is_obstacle(self, pos):
        try:
            return self.level_map[pos[1]][pos[0]] == '#'
        except IndexError:
            return False

    def is_correct_cell(self, pos):
        x, y = pos
        is_correct_x = 0 <= x < self.width
        is_correct_y = 0 <= y < self.height
        return is_correct_x and is_correct_y

    def update(self):
        self.all_sprites.update()
        self.player_projectile_sprites.update()
        self.enemy_projectile_sprites.update()

    def draw(self):
        self.fill((0, 0, 0))
        self.visible_sprites.draw(self.player)

    @property
    def width(self):
        return len(self.level_map[0])

    @property
    def height(self):
        return len(self.level_map)
