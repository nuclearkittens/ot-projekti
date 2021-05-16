import sys
import pygame as pg

from core.demo import Demo

def main():
    '''Initialises and runs the demo.'''
    pg.init()
    demo = Demo()
    demo.loop()
    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
