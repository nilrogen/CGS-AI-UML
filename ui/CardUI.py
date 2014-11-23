import pygame
from pygame.locals import * 

import util.utilities as util
from uiobjects import *

class Card:
    """ Placeholder """
    def __init__(self, name):
        self.name = name
        self.imagename = filter(lambda c: c not in ' :\'', card["name"])
        self.imagename += '.png'
    
    def getImageName(self):
        return self.imagename

class CardUI(UIObject):
    def __init__(self, parentsurface, card, boundingbox):
        UIObject.__init__(self, parentsurface, boundingbox) 
        self.card = card
        self.image = util.getImage(card.getImageName())
    
    def draw(self):
        self.parentsurface.blit(self.image, self.pos)
        



