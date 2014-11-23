import pygame
from pygame.locals import *

import util.utilities as util

class UIObject(object):

    def __init__(self, parent, boundingbox):
        self.parent = parent
        self.bb = boundingbox

        self.children = None
        self.surface = None

        self.pos = (self.bb.x, self.bb.y)
        self.x, self.y = self.bb.x, self.bb.y

        if self.parent:
            self.parent.addChild(self)

    def draw(self):
        pass

    def getPosition(self):
        return self.pos

    def getBoundingBox(self):
        return self.bb


class UICard(UIObject):
    def __init__(self, parent, card, boundingbox):
        uiobject.__init__(self, parent, boundingbox)
        self.card = card
        self.image = util.getImage(card.getImageName())

    def draw(self):
        self.parent.surface.blit(self.image, self.pos)

class Card(object):
    """ Placeholder """
    def __init__(self, name):
        self.name = name
        self.imagename = filter(lambda c: c not in ' :\'', card["name"])
        self.imagename += '.png'

    def getImageName(self):
        return self.imagename






