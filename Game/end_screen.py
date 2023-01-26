import csv
import utils
from settings import *
import pygame
import pygame_gui


class ScoreTable(pygame_gui.elements.UITextBox):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ''

    def load_data(self):
        text = ''
        with open('score.csv') as f:
            reader = csv.reader(f)
            h_name, h_score = reader.__next__()
            text += f'    | {h_name.ljust(33)} | {h_score} \n'
            text += '-' * 48 + '\n'
            for i, row in enumerate(reader):
                name, score = row
                text += f' {str(i + 1).rjust(2)} | {name.ljust(33)} | {score.rjust(5)} \n'
        self.text = text
        self.set_text(text)

    def add_row(self, name, score):
        with open('score.csv') as f:
            reader = csv.reader(f)
            header, *data = list(reader)
            data.append([name, score])
            data.sort(key=lambda x: -int(x[1]))
        with open('score.csv', mode='w', newline='', encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
        self.load_data()

    def update(self, time_delta: float):
        super().update(time_delta)


class EndScreen(pygame.Surface):
    def __init__(self, score):
        self.score = score
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_quit = False

        super().__init__(SIZE)
        self.fill('black')
        self.manager = pygame_gui.UIManager(SIZE)
        # score table
        rect = pygame.Rect(WIDTH * 0.65 / 2, 25, WIDTH * 0.35, HEIGHT * 0.6)
        self.score_table = ScoreTable(manager=self.manager, relative_rect=rect, html_text='')
        self.score_table.load_data()

        # input
        rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT * 0.65, 200, 40)
        self.name_field = pygame_gui.elements.UITextEntryLine(manager=self.manager, relative_rect=rect)

        # buttons
        rect = pygame.Rect(WIDTH / 2 - 150, HEIGHT * 0.75, 300, 80)
        self.write_btn = pygame_gui.elements.UIButton(text='Write', manager=self.manager, relative_rect=rect)

        rect = pygame.Rect(WIDTH * 0.25 - 75 - 150, HEIGHT * 0.75, 300, 80)
        self.restart_btn = pygame_gui.elements.UIButton(text='Restart', manager=self.manager, relative_rect=rect)

        rect = pygame.Rect(WIDTH * 0.75 + 75 - 150, HEIGHT * 0.75, 300, 80)
        self.quit_btn = pygame_gui.elements.UIButton(text='Quit', manager=self.manager, relative_rect=rect)

        # label
        rect = pygame.Rect(WIDTH * 0.25 - 75 - 150, HEIGHT * 0.25, 70, 70)
        self.score_label = pygame_gui.elements.UITextBox(manager=self.manager,
                                                         relative_rect=rect,
                                                         html_text=f'Score\n{score}')

        self.main_cycle()

    def event_handler(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.is_quit = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.write_btn:
                    self.score_table.add_row(self.name_field.get_text(), self.score)
                    self.score_table.load_data()
                    self.name_field.visible = False
                    self.write_btn.visible = False
                if event.ui_element == self.restart_btn:
                    self.running = False
                if event.ui_element == self.quit_btn:
                    self.running = False
                    self.is_quit = True
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
