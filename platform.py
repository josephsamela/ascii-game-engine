from engine import Sprite

class Platform(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(self, pos_x, pos_y)
        self.solid = True
