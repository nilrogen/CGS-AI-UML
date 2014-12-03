import pygame
from pygame.locals import *

import util.utilities as util

class UIObject(object):
    def _updatePosData(self):
        self.pos = (self.bb.x, self.bb.y)
        self.x, self.y = self.bb.x, self.bb.y
        self.w, self.h = self.bb.w, self.bb.h
        self.bbmoved = True

    def __init__(self, boundingbox):
        self.bb = boundingbox
        self.bbmoved = False
        self.pos = (self.bb.x, self.bb.y)
        self.x, self.y = self.bb.x, self.bb.y
        self.w, self.h = self.bb.w, self.bb.h
    
    def changeBoundingBox(self, boundingbox):
        self.bb = boundingbox
        self._updatePosData()

    def move(self, pos):
        self.bb.x, self.bb.y = pos
        self._updatePosData()

    def moveCenter(self, bb):
        if bb.contains(self.bb) == False:
            self.bb.clamp_ip(self.bb)
        else:
            self.bb.center = bb.center
        self._updatePosData()

    def getPosition(self):
        return self.pos

    def getBoundingBox(self):
        return self.bb

    def draw(self, surface):
        pass

class UISurfaceObject(UIObject):

    def __init__(self, surface, boundingbox):
        super(UISurfaceObject, self).__init__(boundingbox)
        self.surface = surface
        self.scaled = False
        self.moved = False

    def draw(self, surface):
        if self.moved:
            surface.blit(surface, self.prevbb.topleft, self.prevbb)
            self.moved = True
        if not self.scaled:
            self.surface = pygame.transform.smoothscale(self.surface, self.bb.size)
            self.scaled = True

        surface.blit(self.surface, self.pos)
   
    def changeBoundingBox(self, boundingbox):
        self.moved = True
        self.scaled = False
        self.prevpos = self.pos
        super(UISurfaceObject, self).changeBoundingBox(boundingbox)
    
    def move(self, pos):
        self.moved = True
        self.prevbb = self.bb
        super(UISurfaceObject, self).move(pos)

    def moveCenter(self, bb):
        self.moved = True
        self.prevbb = self.bb
        super(UISurfaceObject, self).moveCenter(bb)
   

class UICachedImageObject(UISurfaceObject):
    def __init__(self, imagename, boundingbox):
        super(UICachedImageObject, self).__init__(None, boundingbox)
        self.loaded = False
        self.imagename = imagename

    def draw(self, surface):
        if not self.loaded:
            self.surface = util.getImage(self.imagename)
            self.loaded = True
        super(UICachedImageObject, self).draw(surface)
     
class UICard(UICachedImageObject):
    def __init__(self, card, boundingbox):
        super(UICard, self).__init__(card.getImageName(), boundingbox)
        self.card = card

    def getName(self):
        return self.card.name

class Card(object):
    """ Placeholder """
    def __init__(self, name):
        self.name = name
        self.imagename = filter(lambda c: c not in ' .:\'', name)
        self.imagename += '.png'

    def getImageName(self):
        return self.imagename





