import sys

import utils
from settings import *

import pygame
from level import Level
from start_screen import StartScreen
from end_screen import EndScreen


class Game:
    """ Game class """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_quit = False
        # path to level file
        # set in StartScreen
        self.f_level = ''

    def start(self):
        StartScreen(self)
        while True:
            self.game_cycle()
            EndScreen(self.level.score)
            self.running = True

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.is_quit = True

    def game_cycle(self):
        self.level = Level(self, self.f_level)  # load level
        while self.running:
            self.clock.tick(FPS)
            self.event_handler()
            self.level.draw()
            self.level.update()
            self.screen.blit(self.level, (0, 0))
            pygame.display.flip()
        if self.is_quit:
            utils.terminate()
