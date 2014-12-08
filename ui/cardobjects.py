"""
" AUTHOR: Michael Gorlin
" DATE:   2014-11-29
"
" This module contains the class definitions for relevant card
" display areas. These include primarily the hand and battlefield
" views.
"""
import pygame
from pygame.locals import *

import util.utilities as util

from ui.uiobjects import *
from ui.mousehandler import *

#from hearthbreaker.game_objects import Game, Card, Minion


class UICard(UICachedImageObject):
    def __init__(self, card, boundingbox):
        super().__init__(card.imagename, boundingbox)
        self.card = card

    def getName(self):
        return self.card.name


class CardRegion(UICachedImageObject):
    """
    " This class will serve as the basis for all card image views.
    " Primary examples being the hand and the battlefield.
    """
    def __init__(self, boundingbox, bgimagename, gameobj):
        """
        " boundingbox - pygame.Rect
        " bgimagename - string, the name of the background image (*.png)
        " game - The game state DUNNO WHAT THIS WILL BE LIKE.
        """
        super().__init__(bgimagename, boundingbox)
        self.gameobj = gameobj
        self.cardbbs = []
        self._initBoundingBoxes()

    def _initBoundingBoxes(self):
        """
        " This method generates the boundingboxes for images
        " and stores them in self.cardbbs. This method is
        " called in CardRegion.__init__, it only needs to be
        " overridden.
        """
        pass

class UIHandObject(CardRegion):
    """ IM GOING TO HARDCODE THESE VALUES FUCK IT """
    def __init__(self, bb, bgimagename, player):
        super().__init__(bb, bgimagename, player)
        self.order = [i for i in range(10)]
        self.nextbb = None
        self.numcards = 0
        self.cards = []
        self.uicards = []

    def _initBoundingBoxes(self):
        for dx in range(0, 1000, 100):
            self.cardbbs.append(pygame.Rect(dx, 0, 200, 300))

    def _constructSurface(self):
        super()._constructSurface()
        for i in range(self.numcards):
            self.uicards.append(UICard(self.cards[i], self.cardbbs[i]))
        for card in self.uicards:
            card.draw(self.surface)
        """
        dbb = max(5-self.numcards, 0)
        uic, card = None, None
        if len(self.cards) > len(self.uicards):
            self.uicards.append(UICard(self.cards[-1], pygame.Rect(0, 0, 200, 300)))
        for i in range(self.numcards):
            uic = self.uicards[i]
            card = self.cards[i]

            if card.imagename != uic.imagename:
                self.uicards.remove(uic)
                uic = self.uicards[i]
            uic.changeBoundingBox(self.cardbbs[i+dbb])
            uic.draw(self.surface)
        """
    def draw(self, surface):
        super().draw(surface)
        for card in self.uicards:
            card.draw(self.surface)
        
    def drawCard(self):
        card = self.gameobj.draw()
        if card is not None:
            self.cards.append(card)
            self.numcards += 1
            self.forceUpdate()

    def discard(self):
        card = self.gameobj.discard()
        if card is not None:
            self.cards.remove(card)
            self.numcards = len(self.cards)
            self.forceUpdate()
    
            
        


        


        


        


        

    

        
        
        
        




