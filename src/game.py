import pygame

class Game:
    def __init__(self, clock, renderer):
        self.running = True
        self.playing = False

        self._clock = clock
        self._renderer = renderer

        self.UP, self.DOWN, self.RIGHT, self.LEFT = False, False, False, False
        self.SELECT, self.START, self.BACK, self.PAUSE = False, False, False, False

    def start(self):
        self.playing = True

    def game_loop(self):
        while self.playing:
            self.check_events()
            self._render()
            self.reset_keys()
            self._clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.UP = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.DOWN = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.RIGHT = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.LEFT = True
                if event.key == pygame.K_RETURN:
                    self.SELECT = True
                if event.key == pygame.K_p:
                    self.PAUSE = True

    def reset_keys(self):
        self.UP, self.DOWN, self.RIGHT, self.LEFT = False, False, False, False
        self.SELECT, self.START, self.BACK, self.PAUSE = False, False, False, False

    def _render(self):
        self._renderer.render()


        