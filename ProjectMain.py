import os
import random

import pygame
from pygame.locals import *

import util.utilities as util

from ui.application import Application
from ui.uiobjects import tmpCard
from ui.cardobjects import UIHandObject, CardView, UIHero
from ui.mana import ManaRegion
from ui.minion import MinionBase


# Constant Values
WINDOW_SIZE = (1900, 1000)

MANA_PLAYER_LOC = (1490, 950)
MANA_OPPONENT_LOC = (0, 0)

PLAYER_HAND_LOC = (375, 780)
OPPONENT_HAND_LOC = (410, 0)

HERO_POWER_LOC = (1700, 700)

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

    def __init__(self, player, windowsize=WINDOW_SIZE): # 1900x1000
        super().__init__(windowsize)
        self.hand = UIHandObject.createDefaultHandRegion(PLAYER_HAND_LOC, player, False)
        self.manacurrent = ManaRegion.createDefaultManaRegion(MANA_PLAYER_LOC)
        self.manacurrent._setMana(4,10)
        self.cardmouseoverview = CardView('tmpbg.png', None, (0, 640))
        self.hero = UIHero(None, HERO_POWER_LOC)
        
    def HandleMouseEvent(self, event):
        if self.hand.containsPoint(event.pos):
            self.hand.HandleMouseEvent(event)
            mo = self.hand.getMousedOverCard()
            if mo is None:
                self.cardmouseoverview.reset()
            else:
                self.cardmouseoverview.changeCard(mo)
        elif self.hero.heropowerbutton.containsPoint(event.pos):
            self.hero.heropowerbutton.HandleMouseEvent(event)
        else:
            self.hand.removeMouseOver()
            self.cardmouseoverview.reset()

    def onKeydown(self, event):
        if event.key == K_q:
            self.running = False
        elif event.key == K_d:
            self.hand.drawCard()
        elif event.key == K_f:
            self.hand.discard()
        elif event.key == K_s:
            self.hand.toggleShow()

    def render(self):
        self.hand.draw(self._display)
        self.manacurrent.draw(self._display)
        self.cardmouseoverview.draw(self._display)
        self.hero.draw(self._display)
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

