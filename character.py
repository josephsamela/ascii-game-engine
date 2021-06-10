from os import terminal_size
from typing import Text
from engine import Sprite, Animation
from ui import Text

class SpeechBubble(Text):
    def __init__(self, game, player):
        super().__init__(game, 0, 0, '')
        self.text = ''
        self.player = player
    def speak(self, text):
        self.text = text
        self.update()
        self.add(layer='ui')
    def update(self):
        self.pos_x = self.player.pos_x + 3 - len(self.text)/4
        self.pos_y = self.player.pos_y+2
        super().update(self.text)
    def stop(self):
        self.speech.remove()

class Character(Sprite):
    def __init__(self, game, pos_x, pos_y):
        super().__init__(game, 'blank', pos_x, pos_y, transparent=True)
        self.direction = 'right'
        
        self.speechbubble = SpeechBubble(game, self) # Initialize empty speech bubble

        self.animation_walk_left = Animation([
            Sprite(self.game, 'character_walk1', self.pos_x, self.pos_y, invert=True),
            Sprite(self.game, 'character_walk2', self.pos_x, self.pos_y, invert=True)
        ])

        self.animation_walk_right = Animation([
            Sprite(self.game, 'character_walk1', self.pos_x, self.pos_y),
            Sprite(self.game, 'character_walk2', self.pos_x, self.pos_y)
        ])

        self.animation_idle_right = Animation([
            Sprite(self.game, 'character_idle', self.pos_x, self.pos_y)
        ])

        self.animation_idle_left = Animation([
            Sprite(self.game, 'character_idle', self.pos_x, self.pos_y, invert=True)
        ])

        self.animation = self.animation_idle_right
        self.texture = self.animation.texture

    def speak(self, text):
        self.speechbubble.speak(text)

    def update(self):
        # Update animation
        self.animation.next()
        self.texture = self.animation.texture
        # Reposition speach bubble
        self.speechbubble.update()

    def jump(self):
        self.animation = self.animation_idle_right
        self.pos_y -= 5
        self.update()

    def idle(self):
        if self.direction == 'left':
            self.animation = self.animation_idle_left
        elif self.direction == 'right':
            self.animation = self.animation_idle_right
        self.update()

    def move_L(self, dist):
        self.animation = self.animation_walk_left
        self.pos_x -= dist
        self.direction = 'left'
        self.update()

    def move_R(self, dist):
        self.animation = self.animation_walk_right
        self.pos_x += dist
        self.direction = 'right'
        self.update()

    def down(self, dist):
        self.pos_y += dist
        if self.pos_y >= 11:
            self.pos_y = 11
        self.update()
