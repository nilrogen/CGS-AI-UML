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

    def moveRel(self, dx, dy):
        self.bb.x += dx
        self.bb.y += dy
        self._updatePosData()

    def moveCenter(self, bb):
        self.bb.center = bb.center
        self._updatePosData()

    def getPosition(self):
        return self.pos

    def getBoundingBox(self):
        return self.bb

    def fixPosition(self, to):
        """ Fixes position of object to be inside the bounds of
            the to argument. """ 
        self.bb.clamp_ip(to)
        self._updatePosData()

    def containsPoint(self, pos):
        return self.bb.collidepoint(pos)

    def draw(self, surface):
        pass

class UIScaleObject(UIObject):
    """ TODO: Evaluate the usefullness of this subclass. I actually don't
        Know what it does. """


    def __init__(self, surface, boundingbox):
        super(UIScaleObject, self).__init__(boundingbox)
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
        super(UIScaleObject, self).changeBoundingBox(boundingbox)
    
    def move(self, pos):
        self.moved = True
        self.prevbb = self.bb
        super(UIScaleObject, self).move(pos)

    def moveCenter(self, bb):
        self.moved = True
        self.prevbb = self.bb
        super(UIScaleObject, self).moveCenter(bb)

class UISurfaceObject(UIObject):
    def __init__(self, boundingbox):
        super(UISurfaceObject, self).__init__(boundingbox)
        self.surface = None
        self.created = False

    def forceUpdate(self):
        self.created = False

    def _constructSurface(self):
        pass

    def draw(self, surface):
        if self.created == False:
            self.created = True
            self._constructSurface()


class UICachedImageObject(UISurfaceObject):
    def __init__(self, imagename, boundingbox):
        super(UICachedImageObject, self).__init__(boundingbox)
        self.imagename = imagename

    def _constructSurface(self):
        if self.surface is None:
            self.surface = util.getImage(self.imagename)
        self.surface = pygame.transform.smoothscale(self.surface, self.bb.size)

    def draw(self, surface):
        super(UICachedImageObject, self).draw(surface)
        surface.blit(self.surface, self.pos)
     
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
        self.imagename = ''.join(self.imagename) + '.png'

    def getImageName(self):
        return self.imagename





