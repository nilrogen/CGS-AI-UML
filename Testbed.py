import pygame
from pygame.locals import *

import util.utilities as util
from ui.application import * 
from ui.uiobjects import *
from ui.minion import MinionTemp

WINSIZE = 700, 600

class App(Application):
    def __init__(self, windowsize=(200, 200)):
        super(App, self).__init__(windowsize)
        self.objs = [MinionTemp(pygame.Rect(i, 0, 150, 150), None) for i in range(0, 600, 155)]

    def onKeydown(self, event):
        if event.key == K_q:
            self.running = False

    def render(self):
        for obj in self.objs:
            obj.draw(self._display)
        pygame.display.flip()

if __name__ == '__main__':
    app = App(WINSIZE)
    app.execute()
        


    
