from settings import *
import pygame
from utils import neighbors, vector_to_angle
from .entity import Entity


class BaseEnemy(Entity):
    __image = pygame.Surface((TILESIZE - 15, TILESIZE - 15))
    pygame.draw.rect(__image, 'red', (0, 0, *__image.get_size()))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_direction_delay = 1000
        self.path_to_target = []
        self.stats = {'speed': int,
                      'vision': int}

    def anti_stuck(self):
        if self.collision('vert'):
            self.direction.y *= -1

        if self.collision('hor'):
            self.direction.x *= -1
        self.move()

    def check_target(self):
        if self.distance_to_target_tiles <= self.vision:
            self.path_to_target = self.find_path()
            self.update_direction()

    def update_direction(self):
        if self.path_to_target:
            self.direction = (pygame.Vector2(self.path_to_target.pop()) - pygame.Vector2(self.level_pos)).normalize()
        else:
            self.direction = self.dir_to_target

    def update_angle(self):
        self.rotate_angle = vector_to_angle(self.dir_to_target)

    def find_path(self):
        start, finish = self.level_pos, self.target.level_pos
        distances = [[-1 if col == '#' else float('inf') for col in row] for row in self.level.level_map]
        neighbors_cell_cross = [(0, -1), (-1, 0), (1, 0), (0, 1)]  # cross shifts
        neighbors_cell_diagonal = [(-1, -1), (1, -1), (-1, 1), (1, 1)]  # diagonal shifts
        nodes = {finish: 1}  # value of current nodes
        while nodes:
            new_nodes = {}  # temporary place for values of new nodes
            for node, d in nodes.items():  # list of tuple (node, value)
                x, y = node
                distances[y][x] = min(distances[y][x], d)  # min from current and new value of node

                for dx, dy in neighbors_cell_cross + neighbors_cell_diagonal:  # all shifts
                    next_cell = next_x, next_y = x + dx, y + dy  # index of neighbor
                    if not self.level.is_correct_cell(next_cell):  # correct cell check
                        continue
                    if distances[next_y][next_x] != float('inf'):  # if we know value of node - skip iteration
                        continue

                    if (dx, dy) in neighbors_cell_diagonal:  # if neighbor is diagonal
                        value = 1.4  # sqrt(1 ** 2 + 1 ** 2) - diagonal movement
                    else:
                        value = 1

                    new_nodes[next_cell] = round(d + value, 1)  # dist of prev node + value
            if start in nodes:  # if path to start has been found
                break
            nodes = new_nodes  # reload current nodes
        x, y = start
        path = []
        if distances[y][x] == float('inf'):
            return path

        distances = [[float('inf') if elem == -1 else elem for elem in row] for row in distances]  # replace -1 with inf
        while (x, y) != finish:
            # take neighbor with min value
            x, y = min(neighbors(distances, (x, y)), key=lambda pos: distances[pos[1]][pos[0]])
            path.append((x, y))
        return path[::-1]

    def update(self):
        pass

    @property
    def vision(self):
        return self.stats['vision']

    @property
    def target(self):
        return self.targets.sprite

    @property
    def vector_to_target(self):
        return pygame.Vector2(self.pos) - pygame.Vector2(self.target.pos)

    @property
    def dir_to_target(self):
        return self.vector_to_target.normalize()

    @property
    def distance_to_target(self):
        return self.vector_to_target.length()

    @property
    def distance_to_target_tiles(self):
        return int(self.distance_to_target // TILESIZE)
