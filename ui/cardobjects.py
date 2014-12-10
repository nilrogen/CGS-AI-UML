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
from ui.widgets import *

from hearthbreaker.game_objects import Game, Card, Minion

COLOR_PURPLE = (70, 0, 130)

class UICard(UICachedImageObject):

    def __init__(self, card, boundingbox):
        super().__init__(card.imagename, boundingbox)
        self.card = card

    def changeCard(self, card):
        if self.card != card:
            self.card = card
            self.forceUpdate()

    def forceUpdate(self):
        self.imagename = self.card.imagename

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

    def getMousedOverCard(self):
        pass

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
        self.mouseover = None


    def _initBoundingBoxes(self):
        for dx in range(0, 1000, 100):
            self.cardbbs.append(pygame.Rect(XPAD+dx, YPAD, 140, 210))


    def forceUpdate(self):
        self.cards = self.gameobj.hand
        self.numcards = len(self.cards)
        for i in range(self.numcards):
            if len(self.uicards) <= i:
                self.uicards.append(UICard(self.cards[i], self.cardbbs[i]))
            elif self.uicards[i] == None:
                self.uicards[i] = UICard(self.cards[i], self.cardbbs[i])
            else:
                self.uicards[i].changeCard(self.cards[i])
        super().forceUpdate()

            

    def _constructSurface(self):
        super()._constructSurface()
        pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), 2)
        self.surface.fill(COLOR_PURPLE)

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
                self.mouseover = uic
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

    def getMousedOverCard(self):
        return self.mouseover

EXPANDED_SIZE = (240, 360)

class CardView(UICachedImageObject):
    def __init__(self, bgimage, card, pos):
        super().__init__(bgimage, pygame.Rect(pos, EXPANDED_SIZE))
        if card is not None:
            self.image = UICachedImage(card.imagename, EXPANDED_SIZE)
        else:
            self.image = None

       
    def _constructSurface(self):
        super()._constructSurface()
        self.surface.fill(COLOR_PURPLE)
        pygame.draw.rect(self.surface, (255,255,255), self.surface.get_rect(), 2)
        

    def changeCard(self, card):
        if self.image is None:
            self.image = UICachedImage(card.imagename, EXPANDED_SIZE)
        else:
            self.image.imagename = card.imagename
            self.image.loadedImage = None

    def reset(self):
        self.image = None
        self.forceUpdate()

    def setPos(self, pos):
        self.pos = pos

    def draw(self, surface):
        super().draw(surface)
        if self.image is not None:
            self.image.drawAt(surface, self.pos)
    
HERO_SIZE = (200, 200)
class UIHero(UISurfaceObject):
    def __init__(self, player, pos):
        super().__init__(pygame.Rect(pos, HERO_SIZE))
        self.player = player
        self.heropowerbutton = ShittyButton('Hero Power',
                                            umath.addRect(self.bb, (+5, +5), (-10, -100)),
                                            lambda: player.hero.power.use())

        self.heropowerbutton.enabled = False

    def _constructSurface(self):
        self.surface = pygame.Surface(HERO_SIZE)

        text = pygame.font.SysFont('', 40)
        self.surface.fill(COLOR_PURPLE)

        health = self.player.hero.health
        armor = self.player.hero.armor
        htext = text.render(str(health), True, (255, 255, 255))
        atext = text.render(str(armor), True, (255,255,255))

        self.surface.blit(htext, (5, 150))
        self.surface.blit(htext, (145, 150))
        
    

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.surface, self.pos)
        self.heropowerbutton.draw(surface)

        

    

        
        
        
        




