from config import SCREEN_W, SCREEN_H, FONT_SIZE
from ui.menu import Menu

class TitleScreen():
    def __init__(self, renderer):
        self._renderer = renderer

        options = [
            ('battle', 'battle', 'battle'),
            ('help', 'help', 'help'),
            ('quit', 'quit', 'quit')
        ]
        x = SCREEN_W // 2
        y = SCREEN_H // 2
        self.menu = Menu(options, 0, SCREEN_W, SCREEN_H, x, y)
        self._title_text = self._create_title_text()

    def render(self):
        self.menu.draw(self._renderer)
        for text in self._title_text:
            self._renderer.blit(text[0], text[1])

    def update(self, keys):
        return self.menu.update(keys)

    def _create_title_text(self):
        top = 'untitled rpg:'
        bottom = 'turn-based battle demo'

        top_surf = self._renderer.create_text(top, FONT_SIZE * 2)
        top_rect = top_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 4))
        bottom_surf = self._renderer.create_text(bottom, FONT_SIZE)
        bottom_rect = bottom_surf.get_rect(midtop=(SCREEN_W // 2, SCREEN_H // 3))

        return [(top_surf, top_rect), (bottom_surf, bottom_rect)]
