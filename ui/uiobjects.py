import pygame
from pygame.locals import *

import util.utilities as util


class Drawable:
    """ This class is pretending to be a java style interface!"""
    def draw(self, surface):
        pass

class UIObject(Drawable):
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
    """
    " This abstract class serves as the basis for constructing UIObjects
    " that have underlying pygame.Surface structures that can be generated
    " once and reused each draw call. The only method that needs to be 
    " overridden is _constructSurface, which initializes self.surface
    " into a pygame.Surface object.
    """
    def __init__(self, boundingbox):
        # UIObject
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

class UICachedImage(Drawable):
    """ 
    " Sometimes you want a cached image that you can draw at various positions, 
    " not caring about its bounding box
    """
    def __init__(self, imagename, size):
        self.imagename = imagename
        self.loadedImage = None
        self.pos = (0, 0) # Defaults to (0, 0)
        self.size = size

    def draw(self, surface):
        if self.loadedImage is None:
            self.loadedImage = util.getImage(self.imagename)
            print(self.size)
            self.loadedImage = pygame.transform.smoothscale(self.loadedImage, self.size)
        surface.blit(self.loadedImage, self.pos)

    def drawAt(self, surface, pos):
        self.pos = pos
        self.draw(surface)
        

class UICachedImageObject(UISurfaceObject):
    """
    " This concrete class will store an image and retrieve/convert the image when
    " draw(surface) or _constructSurface() are called. The Utility of this is that
    " when dealing with large lists of UICachedImageObjects the slow operation of
    " retrieving and converting the image to pygame.Surface is not done until it's
    " needed. The image is scaled to the size of the bounding box.
    "
    " NOTE: MG - This class at the moment does not handle error checking. So be 
    " sure to use only valid images (found in the pics path.)
    """
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
     

class tmpCard(object):
    """ Placeholder """
    def __init__(self, name):
        self.name = name
        self.imagename = filter(lambda c: c not in ' .:\'', name)
        self.imagename = ''.join(self.imagename) + '.png'

    def getImageName(self):
        return self.imagename





