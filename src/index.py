import pygame as pg

from demo import Demo

def main():
    pg.init()
    demo = Demo()
    demo.battle = True
    demo.loop()
    pg.quit()

if __name__ == '__main__':
    main()
