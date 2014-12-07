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


class CardRegion(UICachedImageObject):
    """
    " This class will serve as the basis for all card image views.
    " Primary examples being the hand and the battlefield.
    """
    def __init__(self, boundingbox, bgimagename, game)
        """
        " boundingbox - pygame.Rect
        " bgimagename - string, the name of the background image (*.png)
        " game - The game state DUNNO WHAT THIS WILL BE LIKE.
        """
        UICachedImageObject.__init__(self, bgimagename, boundingbosx)
        self.game = game
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

   
def UIHandObject(CardRegion):
    def _initBoundingBoxes(self):
        self.
        




