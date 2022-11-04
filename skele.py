import sys
import pygcurse
import pygame
from pygame.locals import *

WINWIDTH = 40
WINHEIGHT = 50

FPS = 40

win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
pygame.display.set_caption('Window Title')
win.autoupdate = False

clock = pygame.time.Clock()

def main():
    while True:
        win.fill(bgcolor='blue')
        handle_events()
        win.fill('#', 'red', region=(5, 5, 10, 10))
        win.update()
        clock.tick(FPS)
        
def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()