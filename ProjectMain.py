import pygame
from pygame.locals import *

import util.utilities as util

from ui.application import *
#from ui.cardobjects import *

WINDOW_SIZE = (1980, 1080)

class ProjectApplication(Application):

    def __init__(self, windowsize=WINDOW_SIZE):
        super().__init__(windowsize)
    def init(self):
        super().init()
        print(pygame.display.Info())
    
    def onKeydown(self, event):
        if event.key == K_q:
            self.running = False
    

if __name__ == '__main__':
    UIProject = ProjectApplication()
    UIProject.execute()

