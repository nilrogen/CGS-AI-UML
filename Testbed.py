import pygame
from pygame.locals import *

import util.utilities as util
from ui.application import * 
from ui.uiobjects import *
from ui.widgets import *
from ui.minion import * 

import engine


WINSIZE = 700, 600

class App(Application):
    def __init__(self, windowsize=(200, 200)):
        super(App, self).__init__(windowsize)

        self.obj = MinionTemp(pygame.Rect(0, 100, 150, 150), \
                                    Minion('TestMinion', 4, 6))
        def act(x):
            self.obj.minion.buff(x, x)
            self.obj.forceUpdate()

        self.buttons = []
        self.buttons.append(ShittyButton('+1/+1', 
                            pygame.Rect(200, 200,200, 70), lambda: act(1)))
        self.buttons.append(ShittyButton('-1/-1', 
                            pygame.Rect(200, 280,200, 70), lambda: act(-1)))
        self.moving = False

    def onKeydown(self, event):
        key = event.key
        if key == K_q:
            self.running = False

        if self.obj is None:
            return
        minion = self.obj
        ref = minion.minion
        if key == K_a:
            ref.heal(1)
            minion.forceUpdate()
        elif key == K_s:
            if ref.damage(1):
                self.obj = None
            minion.forceUpdate()
        elif key == K_d:
            ref.buff(1, 1)
            minion.forceUpdate()

    def onMouseDown(self, event):
        button = event.button
        pos = event.pos

        if self.obj.bb.collidepoint(pos):
            self.moving = True
        for button in self.buttons:
            if button.containsPoint(pos):
                button.mouseDown()

    def onMouseUp(self, event):
        self.moving = False
        for button in self.buttons:
            if button.containsPoint(event.pos):
                button.mouseUp()

    def onMouseMotion(self, event):
        dx, dy = event.rel
        if self.moving:
            obj = self.obj
            obj.move((obj.x + dx, obj.y + dy))

    def render(self):
        self._display.fill((0, 0, 0))
        self.obj.draw(self._display)
        for button in self.buttons:
            button.draw(self._display)
        pygame.display.flip()


if __name__ == '__main__':
    app = App(WINSIZE)
    app.execute()
        


    
