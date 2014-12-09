import glob
import os

import pygame
from pygame.locals import *
from pygame.transform import *
from pygame.rect import Rect

from ui.application import *
from ui.uiobjects import *
import util.utilities as util

class CardImageViewerApplication(Application):
    
    def __init__(self, cardlist, windowsize=(250, 350)):
        super(CardImageViewerApplication, self).__init__(windowsize)
        self.numimages = len(cardlist)
        self.index = 0
        self.cardbb = Rect(0, 0, 200, 300)
        self.cards = [UICard(c, self.cardbb) for c in cardlist]

    def init(self):
        if super(CardImageViewerApplication, self).init() == False:
            return False
        pygame.key.set_repeat(200, 600)

    def onKeydown(self, event):
        key = event.key
        if key == K_LEFT or key == K_a:
            self.index = (self.index - 1) % self.numimages
        elif key == K_RIGHT or key == K_d:
            self.index = (self.index + 1) % self.numimages
        elif key == K_ESCAPE or key == K_q:
            self.running = False

    def render(self):
        """
        disp = self._display
        card = self.cards[self.index]

        card.moveCenter(self.bb)

        disp.fill((0, 0, 0), self.bb)
        card.draw(disp) 
        """
        UICachedImage('CardBack.png', (200, 300)).draw(self._display)
        pygame.display.flip()

if __name__ == '__main__':
    imagelist = util.getGlobals().getImageList()
    cards = []
    """
    for i in imagelist:
        cards.append(Card(i.split(os.sep)[-1].split('.')[0]))
    """
    app = CardImageViewerApplication(cards)
    app.execute()

