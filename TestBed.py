import pygame
from pygame.locals import *

import json
import os

from ui.application import * 
from ui.uiobjects import *
import util.utilities as util

class ImageViewerApplication(Application):
    
    def __init__(self, imagenames, windowsize=(500, 500)):
        Application.__init__(self, windowsize)
        self.imagenames = imagenames
        self.numimages = len(imagenames)
        self.index = 0
        self.cardjson = None

    
    def init(self):
        if self.numimages == 0:
            return False
        if Application.init(self) == False:
            return False
        pygame.key.set_repeat(500, 100)

    def onKeydown(self, event):
        key = event.key
        if key == K_LEFT or key == K_a:
            self.index = (self.index - 1) % self.numimages
        elif key == K_RIGHT or key == K_d:
            self.index = (self.index + 1) % self.numimages
        elif key == K_ESCAPE or key == K_q:
            self.running = False
       
       
    def getImages(self):
        images = []
        for i in [-1, 1, 0] :
            modindex = (self.index + i) % self.numimages
            images.append(util.getImage(self.imagenames[modindex]))
        return images

    def render(self):
        images = self.getImages()
        disp = self._display

        disp.fill((0, 0, 0), pygame.Rect(0, 0, self.w, self.h))

        locs = [(0, 0), (200, 0), (100, 100)]
        for i in range(len(images)):
            timg = pygame.transform.smoothscale(images[i], (200, 300))
            timg.set_alpha(50)
            disp.blit(timg, locs[i])
        pygame.display.flip()

if __name__ == '__main__':
    imagelist = util.getGlobals().getImageList()
    app = ImageViewerApplication(imagelist)
    app.execute()
        
        
        

            

        
