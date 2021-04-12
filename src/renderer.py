import pygame

class Renderer:
    def __init__(self):
        self.SCREEN_W = 512
        self.SCREEN_H = 448
        self.FONT_NAME = 'assets/m5x7.ttf'
        self.DARK_PURPLE = (66, 30, 66)
        self.POWDER_ROSE = (201, 143, 143)
        self.DARK_ROSE = (189, 113, 130)

        self.screen = pygame.Surface((self.SCREEN_W,self.SCREEN_H))
        self.display = pygame.display.set_mode(((self.SCREEN_W,self.SCREEN_H)))


    def draw_text(self, text, size, x, y, colour=None):
        if not colour:
            colour = self.POWDER_ROSE
        font = pygame.font.Font(self.FONT_NAME, size)
        text_surf = font.render(text, False, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surf, text_rect)

    def draw_cursor(self, cursor, size=32):
        self.draw_text(cursor.cursor, size, cursor.rect.x, cursor.rect.y)

    def blit_screen(self):
        self.display.blit(self.screen, (0,0))

    def update(self):
        pygame.display.update()

    def fill(self, colour=None):
        if not colour:
            colour = self.DARK_PURPLE
        self.screen.fill(colour)


    