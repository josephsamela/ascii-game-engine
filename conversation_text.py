import time
from engine import Engine, Sprite
from ui import UI
from controller import Controller

class Conversation:
    def __init__(self, game):
        
        self.sprite = Speech(game, 'Jak: Hello traveler! Welcome to my shop.')
        # Speech('Jak: Need to buy something?')
        # rsp = Decision()
        # if rsp == 'yes':
        #     Speech('Jak: Wonderful! Take a look!')
        # elif rsp == 'no':
        #     Speech('Jak: Ah, perhaps another time. Farewell!')
        
class Speech:
    def __init__(self, game, text):
        self.pos_x = 2
        self.pos_y = 17
        self.text = text
        self.texture = '──────────────────────────────────────────────────────────────\n'+self.text
        game.engine.ui.sprites.append(self.sprite)

class Decision:
    def __init__(self):
        self.pos_x = 57
        self.pos_y = 14
        self.animation_input_yes = Sprite('input_yes', self.pos_x, self.pos_y)
        self.animation_input_no = Sprite('input_no', self.pos_x, self.pos_y)
        self.option = 'yes'
        self.animation = self.animation_input_yes
        self.texture = self.animation.texture

    def set_yes(self):
        self.option = 'yes'
        self.animation = self.animation_input_yes
        self.texture = self.animation.texture

    def set_no(self):
        self.option = 'no'
        self.animation = self.animation_input_no
        self.texture = self.animation.texture

class Game:
    def __init__(self):
        self.engine = Engine(24, 68)

        ui = UI(self)
        ui.setName('Tak The Dwarf')
        ui.setLocation('Forest of Id')
        ui.setHP(3)
        ui.setMP(8)

        kb = Controller()

        self.engine.tick()
        while True:
            self.engine.tick()

            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27: # ESC
                    break
                elif ord(c) == 13: # ENTER
                    pass
                elif c == 'w':
                    ui.input.set_yes()
                elif c == 'a':
                    pass
                elif c == 's': 
                    ui.input.set_no()
                elif c == 'd':
                    pass
                elif c == 'm':
                    ui.startConversation('Hak: Good morning fellow traveler!')
                elif c == 'n':
                    ui.endConversation()
                else:
                    input(ord(c))
            else:
                pass

        kb.set_normal_term()
    
g = Game()
