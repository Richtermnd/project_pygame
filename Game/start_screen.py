import os
import utils
from settings import *
import pygame
import pygame_gui


class StartScreen(pygame.Surface):
    previews = {file.split('.')[0]: f'../levels/{file}'
                for file in os.listdir('../levels')}

    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_quit = False

        super().__init__(SIZE)
        self.fill('black')
        self.manager = pygame_gui.UIManager(SIZE)
        self.start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH * 0.05, HEIGHT * 0.6),
                                                                                (WIDTH * 0.25, HEIGHT * 0.15)),
                                                      text='Start',
                                                      manager=self.manager)
        self.level_select = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((WIDTH * 0.35, HEIGHT * 0.6),
                                                                                         (WIDTH * 0.3, HEIGHT * 0.15)),
                                                               manager=self.manager,
                                                               options_list=os.listdir('../levels'),
                                                               starting_option=os.listdir('../levels')[0])
        self.main_cycle()

    def event_handler(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.is_quit = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_btn:
                    self.running = False
                    self.game.f_level = f'../levels/{self.level_select.selected_option}'
            self.manager.process_events(event)

    def draw(self, time_delta):
        self.manager.update(time_delta)
        self.manager.draw_ui(self)
        self.screen.blit(self, (0, 0))

    def main_cycle(self):
        while self.running:
            self.event_handler()
            self.fill('black')
            self.draw(self.clock.tick(30) / 1000)
            pygame.display.flip()
        if self.is_quit:
            utils.terminate()
