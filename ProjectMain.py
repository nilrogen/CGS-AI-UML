import os

import pygame
from pygame.locals import *

import util.utilities as util

from ui.application import Application
from ui.uiobjects import tmpCard
from ui.cardobjects import UIHandObject

WINDOW_SIZE = (1900, 1000)
import random

class tmpPlayer(object):
    def __init__(self, cards):
        self.cards = cards
        self.hand = []
        self.hsize = 0

    def draw(self):
        if self.hsize >= 10:
            return None
        self.hsize += 1
        self.hand.append(self.cards[random.randint(0, 30)])
        return self.hand[-1]

    def discard(self):
        if self.hsize == 0:
            return None
        self.hsize -= 1
        card = random.choice(self.hand)
        self.hand.remove(card)
        return card

class ProjectApplication(Application):

    def __init__(self, player, windowsize=WINDOW_SIZE):
        super().__init__(windowsize)
        self.hand = UIHandObject(pygame.Rect(400, 800, 1100, 200), 'tmpbg.png', player)
        
    def HandleMouseEvent(self, event):
        if self.hand.containsPoint(event.pos):
            self.hand.HandleMouseEvent(event)
        else:
            self.hand.removeMouseOver()

    def onKeydown(self, event):
        if event.key == K_q:
            self.running = False
        elif event.key == K_d:
            self.hand.drawCard()
        elif event.key == K_f:
            self.hand.discard()

    def render(self):
        self.hand.draw(self._display)
        pygame.display.flip()
    
if __name__ == '__main__':
    imagelist = util.getGlobals().getImageList()
    cards = []
    # TODO: Fix this 
    for i in imagelist:
        cards.append(tmpCard(i.split(os.sep)[-1].split('.')[0]))
    player = tmpPlayer(cards)

    UIProject = ProjectApplication(player, WINDOW_SIZE)
    UIProject.execute()

