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

    def tick(self):
        # Method intended for override by child
        pass

class ScreenBuffer:
    def __init__(self, height, width, h_offset, v_offset):
        # Dimensions of game
        self.height = height
        self.width = width
        self.h_offset = h_offset
        self.v_offset = v_offset
        self.lines = []
        self.sprites = []
        self.clear_buffer()

    def clear_buffer(self):
        # create empty buffer
        self.lines = []
        for h in range(self.height):
            self.lines.append([])
            for w in range(self.width):
                self.lines[h].append(None)

    def draw(self, sprite):
        for offset_y, row in enumerate(sprite.texture):
            for offset_x, col in enumerate(row):
                # Handle sprite transparency
                if sprite.transparent and col == ' ':
                    col = None
                # Calculate texture location
                loc_x = sprite.pos_x + offset_x
                loc_y = sprite.pos_y + offset_y
                # Handle situations where texture location is beyond screen
                if loc_x < 0 or loc_y < 0:
                    continue
                if loc_x >= self.width or loc_y >= self.height:
                    continue
                # Write sprite texture to buffer.=
                self.lines[int(loc_y)][int(loc_x)] = col


    def display(self):
        # Draw all sprites into buffer
        for sprite in self.sprites:
            self.draw(sprite)

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
    def __init__(self, height, width):
        # Game clock
        self.time = time.time()

        # Dimensions of game
        self.height = height
        self.width = width

        # Create screen buffers
        self.ui  = ScreenBuffer(self.height, self.width, 0, 0)
        self.txt = ScreenBuffer(self.height, self.width, 0, 0)
        self.bg  = ScreenBuffer(self.height, self.width, 0, 0)
        self.obj = ScreenBuffer(self.height, self.width, 0, 0)
        self.fg  = ScreenBuffer(self.height, self.width, 0, 0)
        # self.txt = ScreenBuffer(self.height, self.width-6, 2, 3) # These screen buffers are offset because they exist "inside" the UI frame
        # self.bg  = ScreenBuffer(self.height, self.width-6, 2, 3) #
        # self.obj = ScreenBuffer(self.height, self.width-6, 2, 3) #
        # self.fg  = ScreenBuffer(self.height, self.width-6, 2, 3) #
        self.buffers = [self.bg, self.obj, self.fg, self.txt, self.ui]

        self.lines = []
        self.clear_screen()

    def render(self):
        # Clear Engine display buffer
        self.lines = []
        for h in range(self.height):
            self.lines.append([])
            for w in range(self.width):
                self.lines[h].append(None)

        # Composite all buffers
        for b in self.buffers:
            b.display() # Redraw frame
            for h,r in enumerate(b.lines):
                for w,c in enumerate(r):
                    if c == None:
                        continue
                    self.lines[h + b.v_offset][w + b.h_offset] = c

        # Replace all None with ' ' for final print
        for h in range(len(self.lines)):
            for w in range(len(self.lines[h])):
                if self.lines[h][w] == None:
                    self.lines[h][w] = ' '

        # Join screenbuffer into line and print
        l = ''
        for line in self.lines:
            l += ''.join(line) + '\n'
        # Reset cursor position
        for i in range(self.height-1):
            sys.stdout.write("\033[A")
        # Print :)
        print(l[0:-1], end='\r', flush=True)

    def clear_buffer(self):
        for buffer in self.buffers:
            buffer.clear_buffer()

    def clear_screen(self):
        # clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def tick(self):
        # Update clock
        self.time = time.time()
        # Update sprites
        for b in self.buffers:
            for s in b.sprites:
                s.tick()
        # Empty the buffer
        self.clear_buffer()
        self.render()