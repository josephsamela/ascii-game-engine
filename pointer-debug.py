from os import truncate
import time
from engine import Animation, Engine, Sprite
from ui import UI
from controller import Controller
from character import Character

class Game:
    def __init__(self):
        self.engine = Engine(24, 67)
        
        ui = UI(self)
        ui.setName('Taki The Dwarf')
        ui.setLocation('City of Id')
        ui.setHP(10)
        ui.setMP(10)
        
        character = Character(self, 2, 8)
        character.add(layer='obj')

        pointer = Sprite(self, 'pointer', 0, 15, transparent=True)
        pointer.add(layer='obj')

        kb = Controller()

        while True:
            time.sleep(1/30)
            self.engine.tick()

            ui.setName(f'({pointer.pos_x},{pointer.pos_y})')

            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27: # ESC
                    break
                elif ord(c) == 13: # ENTER
                    pass
                elif c == 'w':
                    pointer.pos_y -= 1
                elif c == 'a':
                    pointer.pos_x -= 2
                elif c == 's': 
                    pointer.pos_y += 1
                elif c == 'd':
                    pointer.pos_x += 2

        kb.set_normal_term()
    
g = Game()
