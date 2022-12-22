import math
import pygame

TILESIZE = 48
WIDTH = TILESIZE * 16 * 1.5
HEIGHT = TILESIZE * 9 * 1.5
SIZE = WIDTH, HEIGHT
CENTER = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
FPS = 60

pygame.display.set_mode(SIZE)

FOV = math.pi / 2
HALF_FOV = FOV / 2
# NUM_RAYS = WIDTH // 2
NUM_RAYS = 1
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
