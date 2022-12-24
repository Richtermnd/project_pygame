import os
from .tile import Tile
from utils import load_image


class Wall(Tile):
    _images = {image: load_image(f'tiles\\walls\\{image}')
               for image in os.listdir(r'sprite_images\tiles\walls')}

    def __init__(self, groups, topleft, neighbors):
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
        super().__init__(groups, topleft)
        self.hitbox = self.rect.inflate(-20, -20)




