from engine import Sprite, Animation

class Character:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = 'right'

        self.animation_walk_left = Animation([
            Sprite('character_walk1', self.pos_x, self.pos_y, invert=True),
            Sprite('character_walk2', self.pos_x, self.pos_y, invert=True),
            Sprite('character_walk3', self.pos_x, self.pos_y, invert=True)
        ])

        self.animation_walk_right = Animation([
            Sprite('character_walk1', self.pos_x, self.pos_y),
            Sprite('character_walk2', self.pos_x, self.pos_y),
            Sprite('character_walk3', self.pos_x, self.pos_y)
        ])

        self.animation_idle_right = Animation([
            Sprite('character_idle', self.pos_x, self.pos_y)
        ])

        self.animation_idle_left = Animation([
            Sprite('character_idle', self.pos_x, self.pos_y, invert=True)
        ])

        self.animation = self.animation_idle_right
        self.texture = self.animation.texture

    def jump(self):
        self.animation = self.animation_idle_right
        self.pos_y -= 5
        self.animation.next()
        self.texture = self.animation.texture

    def idle(self):
        if self.direction == 'left':
            self.animation = self.animation_idle_left
        elif self.direction == 'right':
            self.animation = self.animation_idle_right
        self.animation.next()
        self.texture = self.animation.texture

    def move_L(self, dist):
        self.animation = self.animation_walk_left
        self.pos_x -= dist
        self.direction = 'left'
        self.animation.next()
        self.texture = self.animation.texture

    def move_R(self, dist):
        self.animation = self.animation_walk_right
        self.pos_x += dist
        self.direction = 'right'
        self.animation.next()
        self.texture = self.animation.texture

    def down(self, dist):
        self.pos_y += dist
        if self.pos_y >= 11:
            self.pos_y = 11
        self.texture = self.animation.texture
