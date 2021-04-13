import pygame

class EventCheck:
    def __init__(self, gamestate, keys):
        self._gamestate = gamestate
        self._keys = keys

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._gamestate.set_all_false()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._keys.START_K = True
                if event.key == pygame.K_BACKSPACE:
                    self._keys.BACK_K = True
                if event.key == pygame.K_DOWN:
                    self._keys.DOWN_K = True
                if event.key == pygame.K_UP:
                    self._keys.UP_K = True
