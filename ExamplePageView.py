import json
import os

import pygame
from pygame.locals import *

from ui.application import * 
from ui.uiobjects import *
import util.utilities as util

class CardPage(UICachedImageObject):
    def __init__(self, boundingbox, bgimagename, children):
        super(CardPage, self).__init__(bgimagename, boundingbox)

        self.children = []
        cardbb = pygame.Rect(0, 0, 150, 225)

        for card in children:
            self.children.append(UICard(card, cardbb))

    def draw(self, surface):
        super(CardPage, self).draw(surface)
        ypos = 30
        xpos = 30
        
        for i in range(len(self.children)):
            child = self.children[i]
            if i == 4:
                ypos = 255
                xpos = 30
            child.move((xpos, ypos))
            child.draw(self.surface)
            xpos += 170


class ImageViewerApplication(Application):
    
    def __init__(self, cards, windowsize=(500, 500)):
        super(ImageViewerApplication, self).__init__(windowsize)
        self.cards = cards
        self.numimages = len(cards)
        self.index = 0
        self.cardjson = None
    
    def init(self):
        if self.numimages == 0:
            return False
        if Application.init(self) == False:
            return False
        pygame.key.set_repeat(500, 1000)

        bb = pygame.Rect(0, 0, self.w, self.h)
        self.page = CardPage(bb, 'tmpbg.png', cards[:8])

    def onKeydown(self, event):
        key = event.key
        if key == K_LEFT or key == K_a:
            self.index = (8*(self.index - 1)) % self.numimages
            self.changed = True
        elif key == K_RIGHT or key == K_d:
            self.index = (8*(self.index + 1)) % self.numimages
            self.changed = True
        elif key == K_ESCAPE or key == K_q:
            self.running = False
       
       
    def getImages(self):
        images = []
        for i in [-1, 1, 0]:
            modindex = (self.index + i) % self.numimages
            images.append(util.getImage(self.imagenames[modindex]))
        return images

    def render(self):
        #images = self.getImages()
        disp = self._display
        disp.fill((0, 0, 0), pygame.Rect(0, 0, self.w, self.h))
        """
        locs = [(0, 0), (200, 0), (100, 100)]
        for i in range(len(images)):
            timg = pygame.transform.smoothscale(images[i], (200, 300))
            timg.set_alpha(50)
            disp.blit(timg, locs[i])
        """
        self.page.draw(disp)
        pygame.display.flip()

if __name__ == '__main__':
    imagelist = util.getGlobals().getImageList()
    cards = []
    # TODO: Fix this 
    for i in imagelist:
        cards.append(Card(i.split(os.sep)[-1].split('.')[0]))
    app = ImageViewerApplication(cards, (710, 550))
    app.execute()
    
        
        
        

            

        
