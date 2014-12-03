import pygame
from pygame.locals import *

import util.utilities as util
from ui.uiobjects import *

class MouseEventHandler(object):
    def MouseDown(self, event):
        pass

    def MouseUp(self, event):
        pass

    def MouseMove(self, event):
        pass
    
    def HandleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            MouseDown(self, event)
        elif event.type == MOUSEBUTTONUP:
            MouseUp(self, event)
        elif event.type == MOUSEMOTION:
            MouseMove(self, event)


# List of states
_START = 0
# Card Mouse Down
_CMDLMB = 1
_CMDRMB = 2
# Card Mouse Up
_CMULMB = 3
_CMURMB = 4
# BF Mouse Down
_BFMDLMB = 5
_BFMDRMB = 6
# BF Mouse Up
_BFMULMB = 7
_BFMURMB = 8

RIGHTBUTTON = 3
LEFTBUTTON = 1

class CoreMouseHandler(MouseEventHandler):

    def __init__(self, hands, battlefields, engine):
        self.state = _START
        self.hands = hands
        self.battlefields = battlefields
        self.engine = engine

""" TODO: Finish This
    def getItem(self, pos):
        itm = None
        for hand in self.hands:
            itm = hand.(pos)
            if itm is not None:
                return itm
        for bf in self.battlefields:
            itm = hand.getItem(pos)
            if itm is not None:
                return itm
        return itm



    def MouseUp(self, event):
        button = event.button
        pos = event.pos

        
        if self.state == _START:
            if button == LEFTBUTTON:
                itm = self.getItem(pos)
                if itm is None:
                    return
"""

                

        


