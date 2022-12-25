import os
import sys
import math

import pygame
import pygame_gui
import utils


pygame.init()
CANVAS = CW, CH = 1280, 720
INTERFACE = IW, IH = 200, 720
SIZE = W, H = CW + IW, CH
pygame.display.set_mode(SIZE)
GRID_SIZE = GRID_W, GRID_H = 64, 36
TILE_SIZE = CW // GRID_W
all_sprites = pygame.sprite.Group()


class Wall(pygame.sprite.Sprite):
    _images = {image: pygame.transform.scale(utils.load_image(f'tiles\\walls\\{image}'), (TILE_SIZE, TILE_SIZE))
               for image in os.listdir(r'..\sprite_images\tiles\walls')}

    def __init__(self, neighbors, topleft):
        top, bottom = neighbors[0][1] == '#', neighbors[2][1] == '#'
        left, right = neighbors[1][0] == '#', neighbors[1][2] == '#'

        vert = 'row'
        hor = 'col'

        # vert
        if bottom:
            if top:
                vert = 1
            else:
                vert = 0
        elif top:
            vert = 2

        # hor
        if right:
            if left:
                hor = 1
            else:
                hor = 0
        elif left:
            hor = 2

        self.draw_priority = 1
        self.image = Wall._images[f'wall_{vert}{hor}.png']
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        super().__init__(all_sprites)


class Floor(pygame.sprite.Sprite):
    _image = pygame.transform.scale(utils.load_image(r'tiles\floor\floor.png'), (TILE_SIZE, TILE_SIZE))

    def __init__(self, topleft):
        self.draw_priority = 2
        self.image = Floor._image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        super().__init__(all_sprites)


class Interface(pygame.Surface):
    def __init__(self, parent):
        super().__init__(INTERFACE)
        self.parent = parent
        self.rect = pygame.Rect(0, 0, IW, IH)
        self.manager = pygame_gui.UIManager(INTERFACE)
        self.save_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (70, 40)),
                                                     text='Save',
                                                     manager=self.manager)
        self.load_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((110, 20), (70, 40)),
                                                     text='Load',
                                                     manager=self.manager)
        self.brush_decrease = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 80), (70, 40)),
                                                           text='-',
                                                           manager=self.manager)
        self.brush_increase = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((110, 80), (70, 40)),
                                                           text='+',
                                                           manager=self.manager)

    def update(self, time_delta):
        self.fill('black')
        self.manager.update(time_delta)
        self.manager.draw_ui(self)

    def event_handler(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed(3)
        if not self.rect.collidepoint(mouse_pos):
            return
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_btn:
                fd = pygame_gui.windows.UIFileDialog(pygame.Rect((5, 5), (300, 400)), manager=self.parent.gui.manager)
                fd.type = 'save'
            if event.ui_element == self.load_btn:
                fd = pygame_gui.windows.UIFileDialog(pygame.Rect((5, 5), (300, 400)), manager=self.parent.gui.manager)
                fd.type = 'load'
            if event.ui_element == self.brush_increase:
                self.parent.canvas.change_brush_size(1)
            if event.ui_element == self.brush_decrease:
                self.parent.canvas.change_brush_size(-1)

        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            if event.ui_element.type == 'save':
                self.parent.canvas.save(event.text)
            else:
                self.parent.canvas.load(event.text)
        self.manager.process_events(event)


class Canvas(pygame.Surface):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(CANVAS)
        self.map = [['.' for _ in range(GRID_W)] for _ in range(GRID_H)]
        self.update_map()
        self.rect = pygame.Rect(IW, 0, CW, CH)
        self.brush_size = 2

    def update_map(self):
        all_sprites.empty()
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                topleft = x * TILE_SIZE, y * TILE_SIZE
                match col:
                    case '.':
                        Floor(topleft)
                    case '#':
                        Wall(utils.tile_neighbors(self.map, (x, y)), topleft)

    def change_brush_size(self, delta):
        self.brush_size = max(1, min(self.brush_size + delta, 10))

    def is_correct_cell(self, cell):
        x, y = cell
        is_correct_x = 0 <= x < len(self.map[0])
        is_correct_y = 0 <= y < len(self.map)
        return is_correct_x and is_correct_y

    def change_map(self, pos, tile):
        cell_x = (pos[0] - IW) // TILE_SIZE
        cell_y = pos[1] // TILE_SIZE
        start_cell = cell_x, cell_y
        painted_cells = [(cell_x, cell_y)]
        self.map[cell_y][cell_x] = tile
        while painted_cells:
            x, y = painted_cells.pop()
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                cur_cell = cur_x, cur_y = x + dx, y + dy
                if not self.is_correct_cell(cur_cell):
                    continue
                if self.map[cur_y][cur_x] == tile:
                    continue
                if math.dist(cur_cell, start_cell) <= self.brush_size - 1:
                    self.map[cur_y][cur_x] = tile
                    painted_cells.append(cur_cell)
        self.update_map()

    def alt_change_map(self, pos, tile):
        cell_x = (pos[0] - IW) // TILE_SIZE
        cell_y = pos[1] // TILE_SIZE
        cell = cell_x, cell_y
        self.map[cell_y][cell_x] = tile
        r = self.brush_size - 1 if self.brush_size % 2 else self.brush_size
        for neighbor in utils.neighbors(self.map, cell, dist=r):
            if math.dist(neighbor, cell) <= self.brush_size - 1:
                self.map[neighbor[1]][neighbor[0]] = tile
        self.update_map()

    def update(self):
        self.fill('black')
        all_sprites.update()
        all_sprites.draw(self)

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed(3)
        if not self.rect.collidepoint(mouse_pos):
            return

        if mouse_buttons[0]:
            self.alt_change_map(mouse_pos, '#')
        elif mouse_buttons[2]:
            self.alt_change_map(mouse_pos, '.')

    def save(self, path):
        with open(path, mode='w', encoding='UTF-8') as f:
            [print(''.join(row), file=f) for row in self.map]

    def load(self, path):
        with open(path, mode='r', encoding='UTF-8') as f:
            self.map = [list(line) for line in f.readlines()]
        self.update_map()


class MapEditor:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.running = True
        self.clock = pygame.time.Clock()
        self.canvas = Canvas(self)

        self.gui = Interface(self)

    def update(self, time_delta):
        self.canvas.update()
        self.screen.blit(self.canvas, (IW, 0))
        self.gui.update(time_delta)
        self.screen.blit(self.gui, (0, 0))

    def start(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000
            self.event_handler()
            self.update(time_delta)
            pygame.display.flip()
            self.screen.fill('black')
        utils.terminate()

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            self.gui.event_handler(event)
        self.canvas.input()


def main():
    m = MapEditor()
    m.start()


if __name__ == '__main__':
    main()
