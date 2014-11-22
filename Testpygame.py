import glob
import os
import pygame
from pygame.locals import *
import numpy as np


IMGS = glob.glob('pics/*.png')
    
class Application:
    def __init__(self):
        self.running = True
        self.surface_display = None
        self.size = self.weight, self.height = 500, 600

    def on_init(self):
        pygame.init()
        self.surface_display = pygame.display.set_mode(self.size, pygame.DOUBLEBUF, 32)
        self.running = True


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == KEYDOWN:
            self.on_keydown()

    def on_keydown(self):
        pass

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

class ImageApp(Application):
    def __init__(self, imgpathlist):
        Application.__init__(self)
        self.pathlist = imgpathlist
        self.currentImage = None
        self.currentImageIndex = 0


    def on_init(self):
        if len(self.pathlist) == 0:
            pass
        Application.on_init(self)
        self.images = [pygame.image.load(img).convert_alpha() for img in self.pathlist]

        img = self.images[0]
        
        aspw, asph = 200 * 1.5, 300 * 1.5
        self.images = map(lambda img: pygame.transform.smoothscale(img, (int(aspw), int(asph))), \
                          self.images)
        self.currentImage = self.images[self.currentImageIndex]


    def on_event(self, event):
        Application.on_event(self, event) 

    def on_keydown(self):
        key = pygame.key.get_pressed()
        
        if key[K_LEFT] or key[K_a]:
            self.currentImageIndex -= 1
            if self.currentImageIndex < 0:
                self.currentImageIndex += len(self.pathlist)
            self.currentImage = self.images[self.currentImageIndex]
        elif key[K_RIGHT] or key[K_d]:
            self.currentImageIndex += 1
            self.currentImageIndex %= len(self.pathlist)
            self.currentImage = self.images[self.currentImageIndex]
        elif key[K_ESCAPE] or key[K_q]:
            self.running = False

    def on_render(self):
        #self.surface_display.fill((255, 255, 0), pygame.Rect((0, 0, 400, 600)))
        self.surface_display.blit(self.images[self.currentImageIndex - 1], (0, 100))
        self.surface_display.blit(self.images[ \
                                  (self.currentImageIndex + 1) % len(self.images)], (200, 100))
        self.surface_display.blit(self.currentImage, (100, 0))
        pygame.display.flip()
    
if __name__ == '__main__':
    app = ImageApp(IMGS)
    app.on_execute()
    
    
    


