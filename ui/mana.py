"""
" AUTHOR: Michael Gorlin
" DATE:   2014-12-03
"
" This module contains the ManaRegion class, a UIObject that renders mana symbols
" on the screen.
"""

import pygame
from pygame.locals import *

import util.utilities as util
from ui.uiobjects import *


class ManaRegion(UIObject):
    """
    " The ManaRegion class defines the surface and utilities that manage the drawing
    " of mana symbols on the screen.
    """

    def __init__(self, bb, manafull, manadepleted, mana=0):
        """
        " bb - bounding box
        " manafull - name of the manafull image e.g. manafull.png
        " manadepleted - name of the manadepleted image
        " mana - starting mana 
        """
        super(ManaRegion, self).__init__(bb)
        self.loaded = False
        self.changed = True
        self.manafullpath = manafull
        self.manadepletedpath = manadepleted
        self.manafull = None
        self.manadepleted = None
        self.manabbs = [pygame.Rect(50*i+bb.x+5, 5+bb.y, 45, 45) for i in range(10)]
        self.currentmana = mana
        self.fullmana = mana
        self.surf = None

    def _loadSurf(self):
        self.surf = pygame.Surface((self.w, self.h))
        pygame.draw.rect(self.surf, (255,255,255), self.bb, 4)
        for i in range(self.fullmana):
            if i < self.currentmana:
                self.surf.blit(self.manafull, self.manabbs[i])
            else: 
                self.surf.blit(self.manadepleted, self.manabbs[i])


    def _setMana(self, current, full):
        self.currentmana = min(current, 10)
        self.fullmana = min(full, 10)
        self.changed = True

    def resetMana(self):
        self._setMana(self.fullmana, self.fullmana)

    def newTurn(self, locked=0):
        newmana = self.fullmana + 1 - locked
        self._setMana(newmana, newmana+locked)

    def useMana(self, amt=1):
        newmana = self.currentmana - amt
        if newmana < 0:
            return True # TODO: Handle this exception
        self._setMana(newmana, self.fullmana)

    def addMana(self, amt=1):
        newmana = self.currentmana + amt
        if newmana > self.fullmana:
            return True # TODO: Handle this exception
        self._setMana(newmana, self.fullmana)

    def draw(self, surface):
        if self.loaded == False:
            self.manafull = util.getImage(self.manafullpath)
            self.manadepleted = util.getImage(self.manadepletedpath)
            self.loaded = True
        if self.changed == True:
            self._loadSurf()
            changed = False
        surface.blit(self.surf, self.bb)


