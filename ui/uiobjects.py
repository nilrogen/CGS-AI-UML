import pygame
from pygame.locals import *

class UIObject:
    def __init__(self, parentsurface, boundingbox):
        self.parentsurface = parentsurface
        self.bb = boundingbox
        self.pos = (self.bb.x self.bb.y)

    def draw(self):
        pass

    def getPosition(self):
        return self.pos

    def getBoundingBox(self):
        return self.bb
