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

HAND_SIZE =  (1050, 220) 
XPAD = 5 
YPAD = 5

class UIHandObject(CardRegion):
    """ IM GOING TO HARDCODE THESE VALUES FUCK IT """
    
    @staticmethod
    def createDefaultHandRegion(pos, player, showhand=True):
        return UIHandObject(pygame.Rect(pos, HAND_SIZE), 'tmpbg.png', player, showhand, 'CardBack.png')

    def __init__(self, bb, bgimagename, player, showhand, cardback):
        super().__init__(bb, bgimagename, player)
        self.numcards = 0
        self.cards = []
        self.cardback = UICachedImage(cardback, (120,180))
        self.showhand = showhand
        self.uicards = []
        self.cardmouseover = None


    def _initBoundingBoxes(self):
        for dx in range(0, 1000, 100):
            self.cardbbs.append(pygame.Rect(XPAD+dx, YPAD, 140, 210))

    def _constructSurface(self):
        super()._constructSurface()
        pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), 2)

        for i in range(self.numcards):
            self.uicards[i].changeBoundingBox(self.cardbbs[i])
            if self.showhand:
                self.uicards[i].draw(self.surface)
            else:
                x, y = self.uicards[i].pos
                self.cardback.drawAt(self.surface, (x, y+10))

    def toggleShow(self):
        self.showhand = not self.showhand
        self.forceUpdate()

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.surface, self.pos)

    def removeMouseOver(self):
        self.cardmouseover = None

    def onMouseMove(self, event):
        normpos = event.pos[0]-self.x, event.pos[1]-self.y
        for uic in reversed(self.uicards):
            if uic.containsPoint(normpos):
                # TODO: Implement Mouseover
                #self.cardmouseover = (uic, umath.addRect(uic.bb, self.bb))
                return
        self.mouseover = None
        
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
    
            
        


        


        


        


        

    

        
        
        
        




