import time
from controller import Controller
from engine import Engine, Sprite

class Game:
    def __init__(self):
        self.engine = Engine(24, 68)

        # Sprites
        ui = Sprite('ui', 0, 0)
        box = Sprite('box', 2, 13)
        background = Sprite('background', 0, 0)

        self.engine.ui.sprites.append(ui)
        self.engine.bg.sprites.append(background)
        self.engine.fg.sprites.append(box)

        kb = Controller()

        self.engine.tick()
        while True:
            time.sleep(1/120)

            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27: # ESC
                    break
                elif c == 'w':
                    box.pos_y -= 1
                elif c == 's':
                    box.pos_y += 1
                elif c == 'a':
                    box.pos_x -= 1
                elif c == 'd':
                    box.pos_x += 1

                self.engine.tick()

        kb.set_normal_term()
    
g = Game()
