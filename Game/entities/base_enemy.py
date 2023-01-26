import utils
from Game.settings import *
import random
import pygame
from utils import neighbors, vector_to_angle, debug
from .entity import Entity


class BaseEnemy(Entity):
    __image = pygame.Surface((TILESIZE - 15, TILESIZE - 15))
    pygame.draw.rect(__image, 'red', (0, 0, *__image.get_size()))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_direction_delay = 500
        self.last_update = random.random() * 500 + pygame.time.get_ticks()
        self.path_to_target = []
        self.is_touch_damage = False

    def move(self):
        """ Move and try to don't stuck"""
        is_stuck = super().move()
        hor, vert = is_stuck
        if hor:
            if not self.direction.y:
                self.hitbox.y += (self.dir_to_target.y / abs(self.dir_to_target.y + 10 ** -5)) * (
                            self.stats['speed'] + 3)
        if vert:
            if not self.direction.x:
                self.hitbox.x += (self.dir_to_target.x / abs(self.dir_to_target.x + 10 ** -5)) * (
                            self.stats['speed'] + 3)

    def update_angle(self):
        self.rotate_angle = vector_to_angle(self.dir_to_target)

    def check_target(self):
        if pygame.time.get_ticks() - self.last_update < self.update_direction_delay:
            return
        # distance check
        if self.dist_to_target_tiles > self.vision:
            return
        self.path_to_target = self.find_path()
        self.last_update = pygame.time.get_ticks()

    def update_direction(self):
        self.check_target()
        if self.path_to_target:
            if self.level_pos == self.next_cell:
                self.next_cell = self.path_to_target.pop()
        else:
            self.direction = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(self.next_cell) - pygame.Vector2(self.level_pos)

    def find_path(self):
        """ Wave algorithm """
        start, finish = self.level_pos, self.target.level_pos
        distances = [[-1 if col == '#' else float('inf') for col in row] for row in self.level.level_map]
        neighbors_cross = [(0, -1), (-1, 0), (1, 0), (0, 1)]  # cross shifts
        neighbors_diagonal = [(-1, -1), (1, -1), (-1, 1), (1, 1)]  # diagonal shifts
        all_neighbors = neighbors_cross + neighbors_diagonal
        nodes = {start: 1}  # value of current nodes
        while nodes:
            new_nodes = {}  # temporary place for values of new nodes
            for node, d in nodes.items():  # list of tuple (node, value)
                x, y = node
                distances[y][x] = min(distances[y][x], d)  # min from current and new value of node

                for dx, dy in all_neighbors:
                    next_cell = next_x, next_y = x + dx, y + dy  # index of neighbor
                    if not self.level.is_correct_cell(next_cell):  # correct cell check
                        continue
                    if distances[next_y][next_x] != float('inf'):  # if we know value of node - skip iteration
                        continue
                    if dx * dy:  # if neighbor is diagonal
                        value = 1.4  # sqrt(1 ** 2 + 1 ** 2) - diagonal movement
                    else:
                        value = 1

                    penalty = 100 * any(map(self.level.is_obstacle,
                                            utils.neighbors(self.level.level_map, next_cell)))
                    new_nodes[next_cell] = round(d + value, 1) + penalty  # dist of prev node + value
            if finish in nodes:  # if path to start has been found
                break
            nodes = new_nodes  # reload current nodes
        x, y = finish
        path = []
        if distances[y][x] == float('inf'):
            return path
        path.append(finish)
        distances = [[float('inf') if elem == -1 else elem for elem in row] for row in distances]  # replace -1 with inf
        while (x, y) != start:
            # take neighbor with min value
            x, y = min(neighbors(distances, (x, y)), key=lambda pos: distances[pos[1]][pos[0]])
            path.append((x, y))
        return path

    def kill(self):
        self.level.score += 10
        self.death_sound.play()
        super().kill()

    def deal_damage(self, damage):
        self.target.change_hp(-damage)

    def update(self):
        super().update()
        self.move()
        self.update_direction()
        self.animation()

    def set_pos(self, topleft):
        super().set_pos(topleft)
        self.next_cell = self.level_pos

    @property
    def vision(self):
        return self.stats['vision']

    @property
    def target(self):
        return self.targets.sprite

    @property
    def vector_to_target(self):
        return pygame.Vector2(self.target.pos) - pygame.Vector2(self.pos)

    @property
    def dir_to_target(self):
        return self.vector_to_target.normalize()

    @property
    def dist_to_target(self):
        return self.vector_to_target.length()

    @property
    def dist_to_target_tiles(self):
        return int(self.dist_to_target // TILESIZE)
