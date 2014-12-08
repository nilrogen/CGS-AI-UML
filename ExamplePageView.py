import json
import os
from copy import copy

import pygame
from pygame.locals import *

import util.utilities as util
from ui.application import * 
from ui.uiobjects import * 
from ui.cardobjects import UICard

class CardPage(UICachedImageObject):
    def __init__(self, boundingbox, bgimagename, cards):
        super(CardPage, self).__init__(bgimagename, boundingbox)

        self.cards = cards
        self.cardbbs = []
        self.children = []

        ypos = 30
        xpos = 30
        for i in range(len(self.cards[0:8])):
            if i == 4:
                ypos = 255
                xpos = 30
            self.cardbbs.append(pygame.Rect(xpos, ypos, 150, 225))
            self.children.append(UICard(self.cards[i], self.cardbbs[i]))
            xpos += 170

    def changeChildren(self, children):
        if len(children) > 8:
            assert(False)
            children = children[0:8]
        self.children = [UICard(children[i], self.cardbbs[i]) for i in range(8)]

    def getCard(self, pos):
        for child in self.children:
            if child.bb.collidepoint(pos): 
                print(child.getName())
                return child 
        return None

    def draw(self, surface):
        super(CardPage, self).draw(surface)
        for child in self.children:
            child.draw(surface)


class ImageViewerApplication(Application):
    
    def __init__(self, cards, windowsize=(500, 500)):
        super(ImageViewerApplication, self).__init__(windowsize)
        self.cards = cards
        self.numimages = len(cards)
        self.index = 0
        self.cardjson = None
        self.page = None
        self.changed = False
    
    def init(self):
        if self.numimages == 0:
            return False
        if Application.init(self) == False:
            return False
        pygame.key.set_repeat(400, 800)
        pygame.mouse.set_visible(True)

        self.page = CardPage(self.bb, 'tmpbg.png', cards[self.index:self.index+8])

    def onKeydown(self, event):
        key = event.key
        if key == K_LEFT or key == K_a:
            self.index = (self.index - 8) % self.numimages
            self.changed = True
        elif key == K_RIGHT or key == K_d:
            self.index = (self.index + 8) % self.numimages
            self.changed = True
        elif key == K_ESCAPE or key == K_q:
            self.running = False

    def onMouseDown(self, event):
        button = event.button
        pos = event.pos
        if button == 1: # Mouse 1
            card = self.page.getCard(pos)
            if card is None:
                return


    def loop(self):
        if self.changed:
            self.changed = False
            self.page.changeChildren(cards[self.index:self.index+8])

    def render(self):
        self.page.draw(self._display)
        pygame.display.flip()

if __name__ == '__main__':
    imagelist = util.getGlobals().getImageList()
    cards = []
    # TODO: Fix this 
    for i in imagelist:
        cards.append(tmpCard(i.split(os.sep)[-1].split('.')[0]))
    app = ImageViewerApplication(cards, (710, 550))
    app.execute()
    
        
        
        

            

        
