from engine import Sprite

class UI:
    def __init__(self, game):

        self.game = game
        self.dialogueActive = False
        self.decisionActive = False

        # Create sprites
        self.ui_border = Sprite(game, 'ui_border', 0, 0, transparent=True)
        self.ui_status = Sprite(game, 'ui_status', 1, 20)
        self.hp = Bar(game, 23, 21, 10)
        self.mp = Bar(game, 37, 21, 10)
        self.name = Text(game, 2, 21, '', width=16, justify='center')
        self.location = Text(game, 49, 21, '', width=16, justify='center')

        self.banner = Sprite(game, 'banner', 2, 2)
        self.banner_health = Bar(game, 21, 2, 25)
        self.banner_text = Text(game, 3, 1, '', width=61, justify='center')

        # Add sprites to layers
        self.ui_status.add(layer='ui')
        self.ui_border.add(layer='ui')
        self.hp.add(layer='ui')
        self.mp.add(layer='ui')
        self.name.add(layer='ui')
        self.location.add(layer='ui')

    def setBanner(self, enable):
        if enable:
            self.banner.add(layer='ui')
            self.banner_health.add(layer='ui')
            self.banner_text.add(layer='ui')
        else:
            self.banner.remove()
            self.banner_health.remove()
            self.banner_text.remove()

    def setHP(self, value):
        self.hp.setValue(value)
    def setMP(self, value):
        self.mp.setValue(value)
    def setName(self, value):
        self.name.update(value)
    def setLocation(self, value):
        self.location.update(value)
    def setBannerText(self, value):
        self.banner_text.update(value)
    def setBannerHealth(self, value):
        self.banner_health.setValue(value)

    def startDecision(self):
        if self.decisionActive == False:
            self.decisionActive = True
            self.decision = Decision(self.game)
            self.decision.add(layer='ui')
    def updateDecision(self):
        if self.decisionActive == True:
            self.decision.remove()
            self.decision = next
            self.decision.add(layer='ui')
    def endDecision(self):
        if self.decisionActive == True:
            self.decision.remove()
            self.decisionActive = False

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
        header = list('───────────────────────────────────────────────────────────────')
        if len(text) < 61:
            line1 = text[0:61]
            line2 = ''
        elif len(text) >= 61:
            # walk back to last " " character and split
            brp = 61
            for i in reversed(text[0:61]):
                if i == " ":
                    break
                else:
                    brp = brp-1
            line1 = text[0:brp]
            line2 = text[brp:122]
        # Add leading space to line to add space
        line1 = ' ' + line1
        line2 = ' ' + line2
        # Pad lines to width
        line1 = line1.ljust(63)
        line2 = line2.ljust(63)
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
    def __init__(self, game):
        super().__init__(game, 'blank', pos_x=58, pos_y=14)
        self.animation_input_yes = Sprite(self.game, 'input_yes', self.pos_x, self.pos_y)
        self.animation_input_no = Sprite(self.game, 'input_no', self.pos_x, self.pos_y)
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
    def __init__(self, game, pos_x, pos_y, value, max_value=10, min_value=0):
        super().__init__(game, 'blank', pos_x, pos_y)
        self.value = value
        self.max_value = max_value
        self.min_value = min_value
        self.texture = None
        self.update()
    def setValue(self, value):
        if self.value > self.max_value:
            self.value = self.max_value
        elif self.value < self.min_value:
            self.value = self.min_value
        else:
            self.value = value
        self.update()
    def update(self):
        self.texture = ['▓'*self.value]
