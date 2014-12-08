"""
" AUTHOR: Michael Gorlin
" DATE:   2014-11-29
"
" This module contains the class definitions for relevant card
" display areas. These include primarily the hand and battlefield
" views.
"""
from copy import copy

import pygame
from pygame.locals import *

import util.utilities as util
import util.math as umath

from ui.uiobjects import *
from ui.mousehandler import *

#from hearthbreaker.game_objects import Game, Card, Minion


class UICard(UICachedImageObject):

    def __init__(self, card, boundingbox):
        super().__init__(card.imagename, boundingbox)
        self.card = card

    def getName(self):
        return self.card.name

    def __str__(self):
        return self.getName()
    def __repr__(self):
        return str(self)


class CardRegion(UISurfaceObject, MouseEventHandler):
    """
    " This abstract class will serve as the basis for all card image views.
    " Primary examples being the hand and the battlefield.
    """
    def __init__(self, boundingbox, bgimagename, gameobj):
        """
        " boundingbox - pygame.Rect
        " bgimagename - string, the name of the background image (*.png)
        " game - The game state DUNNO WHAT THIS WILL BE LIKE.
        """
        super().__init__(boundingbox)
        self.gameobj = gameobj
        self.cardbbs = []
        self.background = UICachedImageObject(bgimagename, pygame.Rect(0, 0, self.w, self.h))
        self._initBoundingBoxes()

    def _initBoundingBoxes(self):
        """
        " This method generates the boundingboxes for images
        " and stores them in self.cardbbs. This method is
        " called in CardRegion.__init__, it only needs to be
        " overridden.
        """
        pass

    def _constructSurface(self):
        self.surface = pygame.Surface(self.bb.size)
        self.background.draw(self.surface)

class UIHandObject(CardRegion):
    """ IM GOING TO HARDCODE THESE VALUES FUCK IT """
    def __init__(self, bb, bgimagename, player):
        super().__init__(bb, bgimagename, player)
        self.order = [i for i in range(10)]
        self.numcards = 0
        self.cards = []
        self.uicards = []
        self.state = 0 # 0 - Start, 1 - MouseOver
        self.cardover = None


    def _initBoundingBoxes(self):
        for dx in range(0, 1000, 100):
            self.cardbbs.append(pygame.Rect(dx, 0, 140, 210))
        self.mouseoversize = (200, 300)

    def _constructSurface(self):
        super()._constructSurface()

        for i in range(self.numcards):
            self.uicards[i].changeBoundingBox(self.cardbbs[i])
            self.uicards[i].draw(self.surface)
        if self.cardover is not None:
            newpos = umath.addPoint(self.cardover.pos, (0, -300))
            self.cardover.changeBoundingBox(pygame.Rect(newpos, self.mouseoversize))
            self.cardover.forceUpdate()
            self.cardover.draw(self.surface)

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.surface, self.pos)

    def removeMouseOver(self):
        self.state = 0
        self.cardover = None
        self.forceUpdate()

    def onMouseMove(self, event):
        normpos = event.pos[0]-self.x, event.pos[1]-self.y
        for uic in reversed(self.uicards):
            print(uic.pos, normpos)
            if uic.containsPoint(normpos):
                print(uic)
                if self.state == 0:
                    self.cardover = copy(uic)
                    self.state = 1
                    self.forceUpdate()
                elif self.cardover != uic:
                    self.cardover = copy(uic)
                    self.forceUpdate()
                return
        self.state = 0 
        self.cardOver = None
        self.forceUpdate()
        
        
    def drawCard(self):
        card = self.gameobj.draw()
        if card is not None:
            self.cards.append(card)
            self.uicards.append(UICard(card, self.cardbbs[self.numcards]))
            self.numcards += 1
            self.forceUpdate()

    def discard(self):
        card = self.gameobj.discard()
        if card is not None:
            self.cards.remove(card)
            self.numcards -= 1
            for uic in self.uicards:
                if uic.card == card:
                    self.uicards.remove(uic)
                    break
            self.forceUpdate()
    
            
        


        


        


        


        

    

        
        
        
        




