from Game.settings import *

import pygame
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level(r'..\levels\level1.txt')

    def start(self):
        self.game_cycle()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def game_cycle(self):
        while self.running:
            self.clock.tick(FPS)
            self.event_handler()

            self.level.draw()
            self.level.update()
            self.screen.blit(self.level, (0, 0))

            pygame.display.flip()