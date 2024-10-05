import os
import sys
import time

class Sprite:
    def __init__(self, game, filename, pos_x, pos_y, invert=False, transparent=False):
        self.game = game
        self.filename = filename
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.invert = invert
        self.transparent = transparent
        
        self.texture = []
        self.load_texture(filename)

        self.dim_x = len(self.texture[0])
        self.dim_y = len(self.texture)
        self.dim_x_drawn = 0
        self.dim_y_drawn = 0

    def load_texture(self, filename, encoding='utf-8'):
        with open(f'sprites/{filename}.txt', 'r') as s:
            # lines = s.readlines()
            lines = s.read().split('\n')
            for line in lines:
                l = []
                for char in line:
                    if char in ['\n', '\r']:
                        continue
                    l.append(char)
                if self.invert:
                    l = l[::-1]
                self.texture.append(l)

    def add(self, layer):
        # Sprite to add itself to layer
        self.layer = layer
        if layer == 'ui':
            self.game.engine.ui.sprites.append(self)
        elif layer == 'txt':
            self.game.engine.txt.sprites.append(self)
        elif layer == 'fg':
            self.game.engine.fg.sprites.append(self)
        elif layer == 'bg':
            self.game.engine.bg.sprites.append(self)
        elif layer == 'obj':
            self.game.engine.obj.sprites.append(self)
            
    def remove(self):
        # Sprite to remove itself from
        if self.layer == 'ui':
            self.game.engine.ui.sprites.remove(self)
        elif self.layer == 'txt':
            self.game.engine.txt.sprites.remove(self)
        elif self.layer == 'fg':
            self.game.engine.fg.sprites.remove(self)
        elif self.layer == 'bg':
            self.game.engine.bg.sprites.remove(self)
        elif self.layer == 'obj':
            self.game.engine.obj.sprites.remove(self)

        self.game.engine.tick()

    def tick(self):
        # Method intended for override by child
        pass

class Layer:
    def __init__(self, name, width, height):
        self.name = name
        self.buffer = Buffer(width, height)
        self.sprites = []

    def draw(self):
        self.buffer.clear()
        for sprite in self.sprites:
            self.buffer.draw(sprite)

    def add(self, sprite):
        self.sprites.append(sprite)
    
    def remove(self, sprite):
        self.sprites.remove(sprite)

class Buffer:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.buffer = None
        self.clear()

    def get(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        else:
            return self.buffer[y][x]

    def set(self, x, y, char):
        # Ignore characters outside buffer bounds
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            pass
        else:
            self.buffer[y][x] = char

    def clear(self):
        self.buffer = []
        for h in range(self.height):
            self.buffer.append([None]*self.width)
        # self.buffer = [[None]*self.width]*self.height

    def draw(self, sprite):
        # Iterate over each character in sprite texture
        for offset_y, row in enumerate(sprite.texture):
            for offset_x, col in enumerate(row):

                # Calculate position of character
                loc_x = sprite.pos_x + offset_x
                loc_y = sprite.pos_y + offset_y

                # Write character to buffer location
                if sprite.transparent and col == ' ':
                    pass
                else:
                    self.set(loc_x, loc_y, col)

class Animation:
    def __init__(self, frames):
        self.frame = 0
        self.frames = frames # list of sprites
        self.texture = self.frames[0].texture
    def next(self):
        self.frame += 1
        if self.frame > len(self.frames)-1:
            self.frame = 0
        self.texture = self.frames[self.frame].texture

class Engine:
    def __init__(self, width, height):
        # Game clock
        self.time = time.time()

        # Dimensions of game
        self.width = width
        self.height = height

        # Dimensions of screen
        self.screen_width, self.screen_height = os.get_terminal_size()
        self.pillarbox = round((self.screen_width - self.width)/2)
        self.letterbox = round((self.screen_height - self.height)/2)

        # Create screen buffers
        self.ui  = Layer('ui', width, height)
        self.txt = Layer('txt', width, height)
        self.bg  = Layer('bg', width, height)
        self.obj = Layer('obj', width, height)
        self.fg  = Layer('fg', width, height)
        self.layers = [self.bg, self.obj, self.fg, self.txt, self.ui]

        self.buffer = Buffer(width, height)
        self.clear_screen()

    def render(self):
        # Composite all layers into a single buffer
        for layer in self.layers:
            layer.draw()
            for y in range(self.height):
                for x in range(self.width):
                    char=layer.buffer.get(x,y)
                    
                    if char != None:
                        self.buffer.set(x, y, char)

        # Formate frame buffer into single line
        letterbox_upper = (' '*self.screen_width+'\n')*(self.letterbox+1)
        letterbox_lower = (' '*self.screen_width+'\n')*(self.letterbox-1)
        l = ''
        for row in self.buffer.buffer:
            # Replace None with ' '
            for i, c in enumerate(row):
                if c == None:
                    row[i] = ' '
            l += ' '*self.pillarbox + ''.join(row) + ' '*self.pillarbox + '\n'
        l = letterbox_upper + l + letterbox_lower

        # Reset cursor position
        for i in range(self.height-1):
            sys.stdout.write("\033[A")

        # Print line
        print(l[0:-1], end='\r', flush=True)

    def clear_screen(self):
        # clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def tick(self):
        # Update clock
        self.time = time.time()
        # Update sprites
        for layer in self.layers:
            for sprite in layer.sprites:
                sprite.tick()
        # Empty the buffer
        self.buffer.clear()
        self.render()
