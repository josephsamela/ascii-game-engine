import time
from controller import Controller
from engine import Engine, Sprite

class Animation:
    def __init__(self, frames):
        self.frame = 0
        self.frames = frames # list of sprites
        self.texture = self.frames[0].texture
    def next(self):
        self.frame += 1
        if self.frame > len(self.frames)-1:
            self.frame = 0
        self.texture = self.frames[self.frame].texture

class Character:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.animation_walk_left = Animation([
            Sprite('character2', self.pos_x, self.pos_y),
            Sprite('character3', self.pos_x, self.pos_y),
            Sprite('character2', self.pos_x, self.pos_y)
        ])

        self.animation_walk_right = Animation([
            Sprite('character1', self.pos_x, self.pos_y),
            Sprite('character2', self.pos_x, self.pos_y),
            Sprite('character3', self.pos_x, self.pos_y)
        ])

        self.animation_idle = Animation([
            Sprite('character1', self.pos_x, self.pos_y)
        ])

        self.animation = self.animation_idle
        self.texture = self.animation.texture

    def jump(self):
        self.animation = self.animation_idle
        self.pos_y -= 5
        self.animation.next()
        self.texture = self.animation.texture

    def idle(self):
        self.animation = self.animation_idle
        self.animation.next()
        self.texture = self.animation.texture

    def move_R(self, dist):
        self.animation = self.animation_walk_right
        self.pos_x += dist
        self.animation.next()
        self.texture = self.animation.texture

    def down(self, dist):
        self.pos_y += dist
        if self.pos_y >= 12:
            self.pos_y = 12
        self.texture = self.animation.texture
            

class Platform(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(self, pos_x, pos_y)
        self.solid = True

class Game:
    def __init__(self):
        self.engine = Engine(24, 68)

        gravity = 1
        maxfallspeed = 200
        maxspeed = 80
        jumpforce = 300
        acceleration = 10 

        # Sprites
        ui = Sprite('ui', 0, 0)
        character = Character(2, 8)
        background = Sprite('background', 0, 0)
        cloud = Sprite('cloud', 0, 0)
        ground = Sprite('ground', 0, 16)

        self.engine.ui.sprites.append(ui)
        self.engine.bg.sprites.append(background)
        self.engine.bg.sprites.append(cloud)
        self.engine.fg.sprites.append(character)
        self.engine.fg.sprites.append(ground)

        kb = Controller()

        self.engine.tick()
        while True:
            time.sleep(1/60)

            character.down(gravity)

            cloud.pos_x += 0.01
            self.engine.tick()

            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27: # ESC
                    break
                elif c == 'w':
                    character.jump()
                elif c == 'a':
                    character.pos_x -= 1
                elif c == 's': 
                     character.pos_y += 1
                elif c == 'd':
                    character.move_R(1)
            else:
                character.idle()

        kb.set_normal_term()
    
g = Game()
