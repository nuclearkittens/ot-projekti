import pygame

class Renderer:
    def __init__(self, display):
        self._display = display
        

    def render(self):
        pygame.display.update()