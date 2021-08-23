import time
from controller import Controller
from character import Character
from engine import Engine, Sprite
from ui import UI

class Game:
    def __init__(self):
        self.engine = Engine(24, 68)

        gravity = 0.25
        maxfallspeed = 200
        maxspeed = 80
        jumpforce = 300
        acceleration = 10 

        # Sprites
        # thing = Thing(self)

        # ui = Sprite('ui', 0, 0)
        ui = UI(self)
        ui.setName('Fin The Human')
        ui.setLocation('Land of Ooo')
        ui.setHP(10)
        ui.setMP(10)

        background = Sprite(self, 'background', 0, 0)
        cloud = Sprite(self,'cloud', 0, 0)
        ground = Sprite(self, 'ground', 0, 14)
        character = Character(self, 2, 8)

        background.add(layer='bg')
        cloud.add(layer='bg')
        ground.add(layer='fg')
        character.add(layer='fg')

        kb = Controller()

        self.engine.tick()
        while True:
            time.sleep(1/60)

            character.down(gravity)

            cloud.pos_x += 0.05
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

