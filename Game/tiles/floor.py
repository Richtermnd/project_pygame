import os
from .tile import Tile
from utils import load_image
import random


class Floor(Tile):
    _images = {image: load_image(f'tiles\\floor\\{image}')
               for image in os.listdir(r'sprite_images\tiles\floor')}

    def __init__(self, groups, topleft):
        self.draw_priority = 2
        self.image = Floor._images['floor.png']
        if random.random() > 0.9:
            self.image = random.choice(list(Floor._images.values()))
        super().__init__(groups, topleft)
