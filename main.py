
# # Viewport dimensions

# height = 22
# width = 68

# # Top border
# print('█'*width)

# # Title
# title = "Hello World"
# space = int(width/2 - len(title)/2)
# print(f'{" "*space} {title} {" "*space}')

# # print
# for i in range(height):
#         print('██'+ ' '*(width-4) +'██')


# # Bottom border
# print('█'*width)

import os
import sys
import time
import threading

class Sprite:
    def __init__(self, filename, pos_x, pos_y):
        self.filename = filename
        self.pos_x = pos_x
        self.pos_y = pos_y 

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
                self.texture.append(l)
                    
class ScreenBuffer:
    def __init__(self, height, width):
        # Dimensions of game
        self.height = height
        self.width = width
        self.lines = []
        self.clear_buffer()
        self.clear_screen()

    def clear_buffer(self):
        # create empty buffer
        self.lines = []
        for h in range(self.height):
            self.lines.append([])
            for w in range(self.width):
                self.lines[h].append(' ')

    def clear_screen(self):
        # clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self, sprite):
        pos_x = sprite.pos_x
        pos_y = sprite.pos_y
        loc_x = 0
        loc_y = 0
        for row in sprite.texture:
            for col in row:
                self.lines[pos_y][pos_x] = col
                pos_x += 1
                loc_x += 1 
            pos_x = sprite.pos_x
            loc_x = 0                  
            pos_y += 1
            loc_y += 1

    def display(self):
        self.print('█'*self.width)
        for line in self.lines:
            self.print(''.join(line))
        self.print('█'*self.width)

    def print(self, line):
        print('██'+line+'██')


class Engine:
    def __init__(self, height, width):

        # Dimensions of game
        self.height = height
        self.width = width

        # List of sprites
        self.sprites = []

        # Create buffer
        self.buffer = ScreenBuffer(self.height, self.width)

        # Start gameloop
        #threading.Thread(target=self.gameloop).start()
        #self.gameloop()

    def tick(self):
        # Run forever
        # while True:
        # Empty the buffer
        self.buffer.clear_buffer()
        # Draw all sprites into buffer
        for sprite in self.sprites:
            self.buffer.draw(sprite)            
        # Clear screen
        self.buffer.clear_screen()
        # Display buffer
        self.buffer.display()
        # input('paused')

class Game:
    def __init__(self):
        self.engine = Engine(22, 68)

        # Sprites
        house = Sprite('house', 10, 7)
        house1 = Sprite('house', 20, 7)
        house2 = Sprite('house', 30, 7)
        inn = Sprite('inn', 48, 12)
        store = Sprite('store', 26, 0)

        box = Sprite('box', 5, 5)

        self.engine.sprites.append(house)
        self.engine.sprites.append(house1)
        self.engine.sprites.append(house2)
        self.engine.sprites.append(inn)
        self.engine.sprites.append(store)

        self.engine.sprites.append(box)


        while True:

            self.engine.tick()

            d = input('Enter direction (wasd):  ')

            if d == 'w':
                box.pos_y -= 1
            elif d == 's':
                box.pos_y += 1
            elif d == 'a':
                box.pos_x -= 2
            elif d == 'd':
                box.pos_x += 2
    
g = Game()
