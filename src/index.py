import sys
import pygame as pg

from demo import Demo

def main():
    '''Initialises and runs the demo.'''
    pg.init()
    demo = Demo()
    demo.title = True
    demo.loop()
    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
