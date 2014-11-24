import json
import os

import pygame
from pygame.locals import *

from ui.application import * 
from ui.uiobjects import *
import util.utilities as util

class CardPage(UIObject):

    def __init__(self, parent, boundingbox, bgimage, children):
        UIObject.__init__(self, parent, boundingbox)
        self.surface = util.getImage(bgimage)

        self.children = []
        cardbb = pygame.Rect(0, 0, 150, 225)

        for child in children:
            self.children.append(UICard(self.surface, child, cardbb))

    def draw(self):
        ypos = 30
        xpos = 30
        
        self.parent.blit(self.surface, self.pos)
        for i in range(len(self.children)):
            child = self.children[i]
            if i == 4:
                ypos = 255
                xpos = 30
            child.move((xpos, ypos))
            child.draw()
            xpos += 170


class ImageViewerApplication(Application):
    
    def __init__(self, cards, windowsize=(500, 500)):
        Application.__init__(self, windowsize)
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
        self.page = CardPage(self._display, bb, 'tmpbg.png', cards[:8])
        


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
        self.page.draw()



        pygame.display.flip()

if __name__ == '__main__':
    imagelist = util.getGlobals().getImageList()
    cards = []
    for i in imagelist[:8]:
        cards.append(Card(i.split('.')[0]))
    app = ImageViewerApplication(cards, (710, 550))
    app.execute()
        
        
        

            

        
