import pygame

TILESIZE = 48
WIDTH = TILESIZE * 16 * 1.5
HEIGHT = TILESIZE * 9 * 1.5
SIZE = WIDTH, HEIGHT
CENTER = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
FPS = 60

pygame.display.set_mode(SIZE)
