import pygame
from pygame.locals import *

import util.utilities as util

class UIObject(object):

    def __init__(self, parent, boundingbox):
        self.parent = parent
        self.bb = boundingbox

        self.children = None
        self.surface = None

        if boundingbox:
            self.pos = (self.bb.x, self.bb.y)
            self.x, self.y = self.bb.x, self.bb.y
            self.w, self.h = self.bb.w, self.bb.h

    def addChild(self, child):
        if child.type is UIObject:
            self.children.append(child)
        else: 
            raise TypeError('Child argument is not of type UIObject')

    def changeBoundingBox(self, boundingbox):
        self.pos = (self.bb.x, self.bb.y)
        self.x, self.y = self.bb.x, self.bb.y
        self.w, self.h = self.bb.w, self.bb.h
        if self.surface:
            self.surface = pygame.transform.smoothscale(self.surface, (self.w, self.h))

    def move(self, pos):
        self.bb.move_ip(pos)
        self.pos = pos 
        self.x, self.y = self.bb.x, self.bb.y
        self.w, self.h = self.bb.w, self.bb.h

    def setSurface(self, surface):
        self.surface = surface
        if self.surface:
            self.surface = pygame.transform.smoothscale(self.surface, (self.w, self.h))

    def getPosition(self):
        return self.pos

    def getBoundingBox(self):
        return self.bb

    def draw(self):
        pass


class UICard(UIObject):
    def __init__(self, parent, card, boundingbox):
        UIObject.__init__(self, parent, boundingbox)

        self.card = card
        self.surface = util.getImage(card.getImageName())
        self.surface = pygame.transform.smoothscale(self.surface, (self.w, self.h))
    
    def draw(self):
        self.parent.blit(self.surface, self.pos)

class Card(object):
    """ Placeholder """
    def __init__(self, name):
        self.name = name
        print name
        self.imagename = filter(lambda c: c not in ' :\'', name)
        self.imagename += '.png'

    def getImageName(self):
        return self.imagename





