"""
" AUTHOR: Michael Gorlin
" DATE:   2014-11-22
"
" This module contains the Application class, which serves as the base for
" pygame applications.
"""
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
        """
        " This method houses the application loop. Do not override this methods.
        """
        if self.init() == False:
            self.running = False
        while self.running:
            # Hopefully looptime will allow this loop to iterate every 20ms
            looptime = pygame.time.get_ticks()
            for event in pygame.event.get():
                self.handleEvent(event)
            self.loop()
            self.render()

            looptime = pygame.time.get_ticks() - looptime
            if looptime <= 20:
                pygame.time.delay(20 - looptime)
        self.cleanup()

