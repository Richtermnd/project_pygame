import math
import os
import sys
import pygame


def angle_to_vector(angle):
    return pygame.Vector2(math.cos(angle), math.sin(angle))


def vector_to_angle(vector: pygame.Vector2):
    acos_a = math.acos(vector.x / vector.length())
    asin_a = math.asin(vector.y / vector.length())
    return acos_a * (asin_a // abs(asin_a) if asin_a != 0 else 1)


def debug(info, surface, index=0):
    font = pygame.font.Font(None, 30)
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(10, 10 + index * 30))
    pygame.draw.rect(surface, 'Black', debug_rect)
    surface.blit(debug_surf, debug_rect)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join(r'..\sprite_images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def tile_neighbors(field, cell):
    cell_x, cell_y = cell
    start_y, end_y = max(0, cell_y - 1), min(len(field), cell_y + 2)
    start_x, end_x = max(0, cell_x - 1), min(len(field[0]), cell_x + 2)
    res = [['.', '.', '.'],
           ['.', '.', '.'],
           ['.', '.', '.']]
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if (x, y) == cell:
                continue
            res[y - cell_y + 1][x - cell_x + 1] = field[y][x]
    return res


def neighbors(field, cell, dist=1):
    cell_x, cell_y = cell
    start_y, end_y = max(0, cell_y - dist), min(len(field), cell_y + dist + 1)
    start_x, end_x = max(0, cell_x - dist), min(len(field[0]), cell_x + dist + 1)
    res = []
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if (x, y) == cell:
                continue
            res.append((x, y))
    return res
