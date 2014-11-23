import pygame
from pygame.locals import *

class Application:
    def __init__(self, windowsize = (500, 500)):
        self.running = True
        self._display = None
        self.size = self.w, self.h = windowsize

    def init(self):
        pygame.init()
        self._display = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.running = True

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            self.onKeydown(event)
        elif event.type == KEYUP:
            self.onKeyup(event)

    def onKeydown(self, event):
        pass
    def onKeyup(self, event):
        pass

    def loop(self):
        pass

    def render(self):
        pass

    def cleanup(self):
        pygame.quit()

    def execute(self):
        if self.init() == False:
            self.running = False
        while self.running:
            looptime = pygame.time.get_ticks()
            for event in pygame.event.get():
                self.handleEvent(event)
            self.loop()
            self.render()

            looptime = pygame.time.get_ticks() - looptime
            if looptime <= 20:
                pygame.time.delay(20 - looptime)
        self.cleanup()


