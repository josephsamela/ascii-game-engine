from os import remove
from engine import Sprite

class UI:
    def __init__(self, game):

        self.game = game
        self.dialogueActive = False

        # Create sprites
        self.ui = Sprite(game, 'ui', 0, 0, transparent=True)
        self.hp = Bar(game, 23, 21, 10)
        self.mp = Bar(game, 37, 21, 10)
        self.name = Text(game, 2, 21, '', width=16, justify='center')
        self.location = Text(game, 49, 21, '', width=16, justify='center')
        self.title = Text(game, 3, 1, '', width=61, justify='center')

        # Add sprites to layers
        self.ui.add(layer='ui')
        self.hp.add(layer='ui')
        self.mp.add(layer='ui')
        self.name.add(layer='ui')
        self.location.add(layer='ui')
        self.title.add(layer='ui')

    def setHP(self, value):
        self.hp.setValue(value)
    def setMP(self, value):
        self.mp.setValue(value)
    def setName(self, value):
        self.name.update(value)
    def setLocation(self, value):
        self.location.update(value)
    def setTitle(self, value):
        self.title.update(value)

    def startConversation(self, text):
        if self.dialogueActive == False:
            self.dialogueActive = True
            self.dialogue = Conversation(self.game, text).sprite
            self.dialogue.add(layer='ui')

    def updateConversation(self, text):
        if self.dialogueActive == True:
            next = Conversation(self.game, text).sprite
            self.dialogue.remove()
            self.dialogue = next
            self.dialogue.add(layer='ui')

    def endConversation(self):
        if self.dialogueActive == True:
            self.dialogue.remove()
            self.dialogueActive = False
        

class Conversation(Sprite):
    def __init__(self, game, text):
        super().__init__(game, 'blank', pos_x=2, pos_y=17)
        self.game = game
        self.sprite = self.buildSprite(text)
    def buildSprite(self, text):
        s = Sprite(self.game, 'textbox', self.pos_x, self.pos_y)
        header = list('──────────────────────────────────────────────────────────────')
        if len(text) < 61:
            line1 = text[0:61]
            line2 = ''
        elif len(text) >= 61:
            line1 = text[0:61]
            line2 = text[61:122]
        # Add leading space to line to add space
        line1 = ' ' + line1
        line2 = ' ' + line2
        # Pad lines to width
        line1 = line1.ljust(61)
        line2 = line2.ljust(61)
        # Convert to lists
        line1 = list(line1)
        line2 = list(line2)
        # Build final texture
        s.texture = [
            header,
            line1,
            line2
        ]
        return s

class Decision(Sprite):
    def __init__(game, self):
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

class Text(Sprite):
    def __init__(self, game, pos_x, pos_y, value, justify='left', width=None):
        super().__init__(game, 'blank', pos_x, pos_y)
        self.justify = justify
        if width == None:
            self.width = len(value)
        else:
            self.width = width
    def update(self, value):
        if self.justify == 'left':
            s = value.ljust(self.width)
        elif self.justify == 'right':
            s = value.rjust(self.width)
        elif self.justify == 'center':
            s = value.center(self.width)
        self.texture = [s]

class Bar(Sprite):
    def __init__(self, game, pos_x, pos_y, value):
        super().__init__(game, 'blank', pos_x, pos_y)
        self.value = value
        self.texture = None
        self.update()
    def setValue(self, value):
        self.value = value
        self.update()
    def update(self):
        self.texture = ['▓'*self.value]