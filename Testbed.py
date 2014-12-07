import pygame
from pygame.locals import *

import util.utilities as util
from ui.application import * 
from ui.uiobjects import *
from ui.widgets import *
from ui.minion import * 

import hearthbreaker.game_objects as go

WINSIZE = 700, 600

class App(Application):
    def __init__(self, windowsize=(200, 200)):
        super(App, self).__init__(windowsize)

        self.obj = MinionTemp(pygame.Rect(0, 100, 150, 150), \
                                    'Test', 
                                    go.Minion(10, 10))

        self.buttons = []
        self.buttons.append(ShittyButton('Damage',
                            pygame.Rect(200, 10, 200, 70), lambda: self.obj.damage(1)))
        self.buttons.append(ShittyButton('Shield', 
                            pygame.Rect(200, 90, 200, 70), lambda: self.obj.shield()))
        """
        self.buttons.append(ShittyButton('Taunt', 
                            pygame.Rect(200, 170, 200, 70), self.obj.taunt))
        """
        self.moving = False

    def onKeydown(self, event):
        key = event.key
        if key == K_q:
            self.running = False

        """
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
        """

    def onMouseDown(self, event):
        button = event.button
        pos = event.pos

        if self.obj.bb.collidepoint(pos):
            self.moving = True
        for button in self.buttons:
            if button.containsPoint(pos):
                button.onMouseDown(event)

    def onMouseUp(self, event):
        self.moving = False
        self.obj.fixPosition(self.bb)
        for button in self.buttons:
            if button.containsPoint(event.pos):
                button.onMouseUp(event)

    def onMouseMove(self, event):
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
        


    
