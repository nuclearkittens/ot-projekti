import pygame

class Cursor:
    def __init__(self, char, h=32, w=32):
        self.cursor = char
        self.rect = pygame.Rect(0, 0, w, h)

    