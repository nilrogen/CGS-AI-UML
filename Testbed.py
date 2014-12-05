import pygame
from pygame.locals import *

import util.utilities as util
from ui.application import * 
from ui.uiobjects import *
from ui.minion import * 

WINSIZE = 700, 600

class App(Application):
    def __init__(self, windowsize=(200, 200)):
        super(App, self).__init__(windowsize)

        self.objs = []
        self.objs.append(MinionTemp(pygame.Rect(0, 100, 150, 150), \
                                    Minion('TestMinion', 4, 6)))
        self.moving = False

    def onKeydown(self, event):
        key = event.key
        if key == K_q:
            self.running = False

        if self.objs == []:
            return
        minion = self.objs[0]
        ref = minion.minion
        if key == K_a:
            ref.heal(1)
            minion.changed = True
        elif key == K_s:
            if ref.damage(1):
                self.objs = []
            minion.changed = True
        elif key == K_d:
            ref.buff(1, 1)
            minion.changed = True

    def onMouseDown(self, event):
        button = event.button
        pos = event.pos

        if self.objs[0].bb.collidepoint(pos):
            self.moving = True

    def onMouseUp(self, event):
        self.moving = False
        print('MouseUP')

    def onMouseMotion(self, event):
        dx, dy = event.rel
        if self.moving:
            obj = self.objs[0]
            obj.move((obj.x + dx, obj.y + dy))
        

    def render(self):
        self._display.fill((0, 0, 0))
        for obj in self.objs:
            obj.draw(self._display)
        pygame.display.flip()

if __name__ == '__main__':
    app = App(WINSIZE)
    app.execute()
        


    
