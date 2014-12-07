import pygame
from pygame.locals import *

from util.math import *
from ui.uiobjects import *
from ui.mousehandler import *

class Widget(UISurfaceObject):
    
    def action(self):
        pass
    

class ShittyButton(Widget, MouseEventHandler):
    
    def __init__(self, text, boundingbox, action):
        super(ShittyButton, self).__init__(boundingbox)
        self.text = text
        self.clicked = False
        self.action = action
    
    def _constructSurface(self):
        self.surface = pygame.Surface(self.bb.size, HWSURFACE)
        text = pygame.font.SysFont('', 40)

        surfrect = self.surface.get_rect()
        boxrect = addRect(surfrect, (1, 1), (-2, -2))

        self.surface.fill((0, 0, 0))
        if self.clicked:
            self.surface.fill((200, 255, 255), boxrect)
        else:
            self.surface.fill((200, 200, 200), boxrect)
    
        textR = text.render(self.text, True, (0, 0, 0))

        shadowrect = addRect(surfrect, (3, 3))
        textrect = centerToRect(textR.get_rect(), surfrect)

        pygame.draw.rect(self.surface, (255, 255, 255), shadowrect, 4)

        self.surface.blit(textR, textrect)
    
    def onMouseDown(self, event):
        self.clicked = True
        self.action()
        self.forceUpdate()

    def onMouseUp(self, event):
        self.clicked = False
        self.forceUpdate()

    def containsPoint(self, pos):
        """ Odd method of preventing button from retaining clicked status
            when on Mouse Up events when the mouse is not over the button. """
        val = super(ShittyButton, self).containsPoint(pos)
        if self.clicked and not val:
            self.clicked = False
            self.forceUpdate()
        return val
            
            

    def draw(self, surface):
        super(ShittyButton, self).draw(surface)
        surface.blit(self.surface, self.pos)

