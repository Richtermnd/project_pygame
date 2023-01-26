from Game.settings import *
import random
import pygame
import utils
import custom_groups
from tiles import Floor, Wall
import entities


def load_map(level_file):
    with open(level_file) as level:
        level_map = [list(row.strip()) for row in level.readlines()]
    return level_map


font = pygame.font.Font(None, 40)


class ScoreCounter(pygame.Surface):
    def __init__(self, level):
        self.level = level
        super().__init__((150, 50), pygame.SRCALPHA)
        self.convert_alpha()

    def update(self):
        pygame.draw.rect(self, 'black', self.get_rect(), border_radius=4)
        pygame.draw.rect(self, 'white', self.get_rect(), 3, border_radius=4)
        text = font.render(str(self.level.score), True, 'gray')
        self.blit(text, (self.get_width() / 2 - text.get_width() / 2,
                         self.get_height() / 2 - text.get_height() / 2))
        self.level.blit(self, (self.level.get_width() - 150, 0))


class Level(pygame.Surface):
    def __init__(self, game, level_file):
        super().__init__(SIZE)
        self.game = game
        self.score = 0
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
        self.score_counter = ScoreCounter(self)
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
        self.spawn_player()

    def spawn_player(self):
        x, y = random.randrange(len(self.level_map[0])), random.randrange(len(self.level_map))
        while self.is_obstacle((x, y)):
            x, y = random.randrange(len(self.level_map[0])), random.randrange(len(self.level_map))
        self.player.set_pos((x * TILESIZE, y * TILESIZE))

    def spawn_enemies(self):
        if len(self.enemies_group) >= 5:
            return
        x, y = random.randrange(len(self.level_map[0])), random.randrange(len(self.level_map))
        while self.is_obstacle((x, y)):
            x, y = random.randrange(len(self.level_map[0])), random.randrange(len(self.level_map))
        entities.BattleBeetle((self.all_sprites, self.enemies_group, self.visible_sprites),
                              self.players_group, self).set_pos((x * TILESIZE, y * TILESIZE))

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

    def level_point(self, pos):
        return int(pos[0] // TILESIZE), int(pos[1] // TILESIZE)

    def update(self):
        self.spawn_enemies()
        self.all_sprites.update()
        self.player_projectile_sprites.update()
        self.enemy_projectile_sprites.update()
        self.score_counter.update()

    def draw(self):
        self.fill((0, 0, 0))
        self.visible_sprites.draw(self.player)

    @property
    def width(self):
        return len(self.level_map[0])

    @property
    def height(self):
        return len(self.level_map)
