import pygame
from pygame.locals import *

import util.utilities as util
from ui.uiobjects import *
from ui.mousehandler import *

class MinionBase(UIObject):
    def __init__(self, bb, minion):
        super(MinionBase, self).__init__(bb)
        self.minion = minion
        self.surface = None

   
class MinionTemp(MinionBase):
    def __init__(self, bb, minion):
        super(MinionTemp, self).__init__(bb, minion)
        self.created = False

    def _create(self):
        font = pygame.font.SysFont('Greek', 15)
        yh = int(2.0 * self.bb.h / 3.0)
        w1, w2 = int(self.bb.w * 0.25), int(self.bb.w * 0.75)

        box1 = pygame.Rect(0, 0, self.w, self.h)
        box2 = pygame.Rect(0,  yh, w1, self.h - yh)
        box3 = pygame.Rect(w2, yh, w2, self.h - yh)

        self.surface = pygame.Surface(self.bb.size)

        #name = font.render('Moo',

        pygame.draw.rect(self.surface, (255,255,255), box1, 2)
        pygame.draw.rect(self.surface, (255,255,255), box2, 2)
        pygame.draw.rect(self.surface, (255,255,255), box3, 2)

    def draw(self, surface):
        if self.created == False:
            self._create()
            self.created = True
        surface.blit(self.surface, self.pos)


    




    



