from engine import Sprite

class UI:
    def __init__(self, game):
        self.sprite = Sprite('ui', 0, 0)
        
        self.game = game

        self.hp = Bar(22, 21, 10)
        self.mp = Bar(36, 21, 10)        
        self.setHP(10)
        self.setMP(10)

        self.name = Text(3, 21, 'Hello')
        self.location = Text(49, 21, 'Hello')

        game.engine.ui.sprites.append(self.sprite)
        game.engine.ui.sprites.append(self.hp)
        game.engine.ui.sprites.append(self.mp)
        game.engine.ui.sprites.append(self.name)
        game.engine.ui.sprites.append(self.location)

    def setHP(self, value):
        self.hp.setValue(value)
    def setMP(self, value):
        self.mp.setValue(value)
    def setName(self, value):
        self.name.update(value)
    def setLocation(self, value):
        self.location.update(value)

    def startConversation(self, text):
        c = Conversation(text).sprite
        self.game.engine.ui.sprites.append(c)

    def updateConversation(self, value):
        pass

    def endConversation(self):
        self.game.engine.ui.sprites.pop()

class Conversation:
    def __init__(self, text):
        self.sprite = self.buildSprite(text)
    def buildSprite(self, text):
        s = Sprite('textbox', 2, 17)
        header = list('──────────────────────────────────────────────────────────────')
        if len(text) < 62:
            line1 = text[0:62]
            line2 = ''
        elif len(text) >= 62:
            line1 = text[0:62]
            line2 = text[62:]
        # Add leading space to line to add space
        line1 = ' ' + line1
        line2 = ' ' + line2
        # Pad lines to width
        line1 = line1.ljust(62)
        line2 = line2.ljust(62)
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

class Text:
    def __init__(self, pos_x, pos_y, value):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = [value]
    def update(self, value):
        self.texture = [value]

class Bar:
    def __init__(self, pos_x, pos_y, value):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value
        self.texture = None
        self.update()
    def setValue(self, value):
        self.value = value
        self.update()
    def update(self):
        self.texture = ['▓'*self.value]