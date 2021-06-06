import os
import sys

class Sprite:
    def __init__(self, filename, pos_x, pos_y, invert=False):
        self.filename = filename
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.invert = invert
        
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
        pos_x = sprite.pos_x
        pos_y = sprite.pos_y
        loc_x = 0
        loc_y = 0
        for row in sprite.texture:
            if pos_y >= self.height: 
                break
            for col in row:
                if pos_x >= self.width:
                    break
                self.lines[int(pos_y)][int(pos_x)] = col
                pos_x += 1
                loc_x += 1
            pos_x = sprite.pos_x
            loc_x = 0
            pos_y += 1
            loc_y += 1

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

        # Dimensions of game
        self.height = height
        self.width = width

        # Create buffer
        self.ui = ScreenBuffer(self.height, self.width, 0, 0)
        self.bg = ScreenBuffer(self.height-7, self.width-6, 2, 3)
        self.fg = ScreenBuffer(self.height-7, self.width-6, 2, 3)
        self.buffers = [self.ui, self.bg, self.fg]

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
            b.display() # Redraw sprites
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
        # Empty the buffer
        self.clear_buffer()
        self.render()