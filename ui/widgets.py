import pygame
from pygame.locals import *

from ui.uiobjects import *

class Widget(UISurfaceObject):
    
    def action(self):
        pass
    

class ShittyButton(Widget):
    
    def __init__(self, text, boundingbox, action):
        super(ShittyButton, self).__init__(boundingbox)
        self.text = text
        self.clicked = False
        self.action = action
    
    def _constructSurface(self):
        self.surface = pygame.Surface(self.bb.size, HWSURFACE)
        text = pygame.font.SysFont('', 40)

        if self.clicked:
            self.surface.fill((200, 255, 255))
        else:
            self.surface.fill((200, 200, 200))
    
        textR = text.render(self.text, True, (0, 0, 0))

        rect1 = self.surface.get_rect()
        rect2 = pygame.Rect(rect1.x+3, rect1.y+3, rect1.w-2, rect1.h-2)
        rect3 = textR.get_rect()
        rect3.center = self.surface.get_rect().center
        pygame.draw.rect(self.surface, (0, 0, 0), rect1, 5)
        pygame.draw.rect(self.surface, (255, 255, 255), rect2, 4)
        self.surface.blit(textR, rect3)
    
    def mouseDown(self):
        self.clicked = True
        self.action()
        self.forceUpdate()

    def mouseUp(self):
        self.clicked = False
        self.forceUpdate()

    def draw(self, surface):
        super(ShittyButton, self).draw(surface)
        surface.blit(self.surface, self.pos)

