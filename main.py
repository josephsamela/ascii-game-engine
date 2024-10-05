import time
from engine import Engine, Sprite, Layer
from ui import UI, Conversation, Dialogue
from controller import Controller
from character import Character
from input import Input

class Game:
    def __init__(self):
        self.engine = Engine(68, 24)

        ui = UI(self)
        ui.setLocation('City of Id')
        ui.setName('Taki The Human')
        ui.setBannerText('Megaloth The Forsaken')
        ui.setBannerHealth(100)
        ui.setBanner(True)

        conversation = Conversation(
            ui,
            dialogue=[
                Dialogue('Hello! It\'s nice to meet you!'),
                Dialogue('Would you like to see my wares?', yes="Here, take a look!", no="Ok, that's fine."),
                Dialogue('Please come again soon!')
            ]
        )

        character = Character(self, 10, 10)
        character.add(layer='fg')

        controller = Input()
        while True:
            self.engine.tick()

            i = controller()

            match i:
                case 'q':
                    break
                case 'c':
                    conversation.talk()
                case 'a':
                    character.move_L(1)
                case 'd':
                    character.move_R(1)

            character.idle()
    
g = Game()
