import time
from controller import Controller
from character import Character
from engine import Engine, Sprite

class Game:
    def __init__(self):
        self.engine = Engine(24, 68)

        gravity = 0.25
        maxfallspeed = 200
        maxspeed = 80
        jumpforce = 300
        acceleration = 10 

        # Sprites
        ui = Sprite('ui', 0, 0)
        background = Sprite('background', 0, 0)
        cloud = Sprite('cloud', 0, 0)
        ground = Sprite('ground', 0, 14)
        character = Character(2, 8)

        self.engine.ui.sprites.append(ui)
        # self.engine.bg.sprites.append(background)
        self.engine.bg.sprites.append(cloud)
        self.engine.fg.sprites.append(ground)
        self.engine.fg.sprites.append(character)

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
                    character.move_L(1)
                elif c == 's': 
                     character.pos_y += 1
                elif c == 'd':
                    character.move_R(1)
            else:
                character.idle()

        kb.set_normal_term()
    
g = Game()
