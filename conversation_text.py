from os import truncate
import time
from engine import Engine, Sprite
from ui import UI
from controller import Controller
from character import Character

class Game:
    def __init__(self):
        self.engine = Engine(24, 68)

        ui = UI(self)
        ui.setName('Tak The Dwarf')
        ui.setLocation('Forest of Id')
        ui.setHP(3)
        ui.setMP(8)

        platform = Sprite(self, 'ground', 10, 10, transparent=True)
        platform.add(layer='bg')

        background = Sprite(self, 'background', 0, 0, transparent=False)
        background.add(layer='bg')

        player = Character(self, 14, 4)
        player.add(layer='fg')

        # scroll = Sprite(self, 'scroll', 2, 2)
        # scroll.add(layer='fg')

        # girl = Sprite(self, 'girl', 21, -10)
        # girl.add(layer='fg')


        kb = Controller()

        self.engine.tick()
        dialoge = 0
        while True:
            time.sleep(1/60)
            self.engine.tick()

            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27: # ESC
                    break
                elif ord(c) == 13: # ENTER
                    pass
                elif c == 'w':
                    player.pos_y -= 1
                elif c == 'a':
                    # player.pos_x -= 1
                    player.move_L(1)
                elif c == 's': 
                    player.pos_y += 1
                elif c == 'd':
                    # player.pos_x += 1
                    player.move_R(1)
                elif c == 'm':
                    # ui.startConversation('Hak: Good morning fellow traveler!')

                    dialoge += 1
                    if dialoge == 1:
                        ui.startConversation('Hak: Good morning fellow traveler!')
                    elif dialoge == 2:
                        ui.updateConversation('Hak: Would you like to buy something?')
                    elif dialoge == 3:
                        ui.updateConversation('Hak: Ha, maybe next time. Farewell! ')
                    elif dialoge >= 4:
                        ui.updateConversation('Hak: Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test')
                    elif dialoge >= 5:
                        ui.endConversation()
                        dialoge = 0

                elif c == 'n':
                    ui.endConversation()
                else:
                    input(ord(c))
            else:
                player.idle()

        kb.set_normal_term()
    
g = Game()
