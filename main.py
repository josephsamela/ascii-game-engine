import time
from engine import Engine, Sprite
from ui import UI
from controller import Controller
from character import Character

class TitleSequence(Sprite):
    def __init__(self, game):
        super().__init__(game, 'scroll', pos_x=2, pos_y=20, transparent=True)
    def tick(self):
        self.pos_y -= 0.1

class Game:
    def __init__(self):
        self.engine = Engine(24, 67)

        ui = UI(self)
        ui.setName('Taki The Dwarf')
        ui.setLocation('City of Id')
        ui.setHP(3)
        ui.setMP(8)

        player = Character(self, 14, 11)
        player.add(layer='obj')

        cloud1 = Sprite(self, 'cloud', 0, 1)
        cloud1.add(layer='fg')

        background = Sprite(self, 'background', 0, 2, transparent=True)
        background.add(layer='bg')

        cloud2 = Sprite(self, 'cloud', 25, 2)
        cloud2.add(layer='bg')

        dock = Sprite(self, 'dock', 0, 14, transparent=True)
        dock.add(layer='fg')

        wave = Sprite(self, 'wave', 0, 18, transparent=True)
        wave.add(layer='bg')

        # s = TitleSequence(self)
        # s.add(layer='txt')

        kb = Controller()

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
                    player.move_L(2)
                    # train.pos_x +=1
                elif c == 's': 
                    player.pos_y += 1
                elif c == 'd':
                    # player.pos_x += 1
                    player.move_R(2)
                    # train.pos_x -=1
                elif c == 'm':
                    dialoge += 1
                    if dialoge == 1:
                        # player.speak('Good morning!')
                        ui.startConversation('Hak: Good morning fellow traveler!')
                    elif dialoge == 2:
                        # player.speak('Would you like to buy something?')
                        ui.updateConversation('Hak: Would you like to buy something?')
                        ui.startDecision()
                    elif dialoge == 3:
                        # player.speak('Ha, maybe next time. Farewell!')
                        ui.updateConversation('Hak: Ha, maybe next time. Farewell! ')
                        ui.endDecision()
                    else:
                        ui.endConversation()
                        dialoge = 0

                elif c == 'n':
                    ui.endConversation()
                else:
                    input(ord(c))
            else:
                player.idle()

            if abs(wave.pos_x) > 60:
                wave.pos_x = 0
            if abs(cloud1.pos_x) > 120:
                cloud1.pos_x = 0
            if abs(cloud1.pos_x) > 60:
                cloud1.pos_x = 10

            wave.pos_x -= 0.1
            cloud1.pos_x += 0.05
            cloud2.pos_x += 0.025


        kb.set_normal_term()
    
g = Game()
