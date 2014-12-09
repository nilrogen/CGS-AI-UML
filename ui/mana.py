"""
" AUTHOR: Michael Gorlin
" DATE:   2014-12-03
"
" This module contains the ManaRegion class, a UIObject that renders mana symbols
" on the screen.
"""
import pygame
from pygame.locals import *
from pygame import Rect

import util.utilities as util
from ui.uiobjects import *

from hearthbreaker.game_objects import Player

MANA_SIZE = (40, 40)
COLOR_FILL = (50, 85, 170)


class TmpGameObject:
    mana = 0
    max_mana = 0

class ManaRegion(UISurfaceObject):
    """
    " The ManaRegion class defines the surface and utilities that manage the drawing
    " of mana symbols on the screen.
    """

    def __init__(self, bb, manafull, manadepleted, player):
        """
        " bb - bounding box
        " manafull - name of the manafull image e.g. manafull.png
        " manadepleted - name of the manadepleted image
        " mana - starting mana 
        """
        super().__init__(bb)
        self.manafull = UICachedImage(manafull, MANA_SIZE)
        self.manadepleted = UICachedImage(manadepleted, MANA_SIZE)
        self.manalocs = [(40*i+5, 5) for i in range(10)]

        # Hearthbreaker values, found on Player.__init__ in game_objects.py
        self.currentmana = player.mana
        self.fullmana = player.max_mana

    def _constructSurface(self):
        self.surface = pygame.Surface(self.bb.size)
        self.surface.fill(COLOR_FILL)
        pygame.draw.rect(self.surface, (255,255,255), self.surface.get_rect(), 4)
        pygame.draw.rect(self.surface, (0, 0, 0), self.surface.get_rect(), 2)
        for i in range(self.fullmana):
            if i < self.currentmana:
                self.manafull.drawAt(self.surface, self.manalocs[i])
            else: 
                self.manadepleted.drawAt(self.surface, self.manalocs[i])


    def _setMana(self, current, full):
        self.currentmana = min(current, 10)
        self.fullmana = min(full, 10)
        self.changed = True
        self.forceUpdate()

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
        super().draw(surface)
        surface.blit(self.surface, self.pos)


    @staticmethod
    def createDefaultManaRegion(pos, gameObj=TmpGameObject()):
        return ManaRegion(Rect(pos, (410, 50)),
                         'ManaFull.png',
                         'ManaDepleted.png', 
                         gameObj)
    

