"""
" AUTHOR: Michael Gorlin
" 
" This is an example of the mana view
"""
import pygame
from pygame.locals import *

import util.utilities as util
from ui.application import * 
from ui.uiobjects import *
from ui.mana import *

class ManaApp(Application):
    def __init__(self, windowsize=(515, 80)):
        super(ManaApp, self).__init__(windowsize)
        self.manaregion = ManaRegion.createDefaultManaRegion((0, 0))
        
    def onKeydown(self, event):
        key = event.key
        if key == K_a:
            self.manaregion.useMana()
        elif key == K_d:
            self.manaregion.addMana()
        elif key == K_w:
            self.manaregion.newTurn(4)
        elif key == K_t:
            self.manaregion.newTurn()
        elif key == K_r:
            self.manaregion.resetMana()
        elif key == K_q:
            self.running = False
            
    def render(self):
        self.manaregion.draw(self._display)
        pygame.display.flip()

ma = ManaApp()
ma.execute()



