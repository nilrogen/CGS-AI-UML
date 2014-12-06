import pygame
from pygame.locals import *

import util.utilities as util
from ui.uiobjects import *
from ui.mousehandler import *

COLOR_WHITE = (255, 255, 255)
COLOR_DAMAGED = (230, 20, 20)
COLOR_BUFFED = (0, 255, 60)
COLOR_BOX_TAUNT = (133, 133, 133)
COLOR_BOX_SHIELD = (255, 255, 0)
COLOR_AURA_SILENCE = (0, 0, 0)
COLOR_AURA_CAN_ATTACK = (0, 0, 0)

class MinionBase(UISurfaceObject):
    def __init__(self, bb, minion):
        super(MinionBase, self).__init__(bb)
        self.minion = minion
   
class MinionTemp(MinionBase):
    def __init__(self, bb, minion):
        super(MinionTemp, self).__init__(bb, minion)

        # Minion Properties

        if minion is not None:
            self.power = minion.getPower()
            self.toughness = minion.getToughness()

    def _getColors(self):
        if self.isTaunt():
            box = COLOR_BOX_TAUNT
        else:
            box = COLOR_WHITE

        if  self.isDamaged():
            toughness = COLOR_DAMAGED
        elif self.isOverhealed():
            toughness = COLOR_BUFFED
        else:
            toughness = COLOR_WHITE

        if self.isBuffed():
            power = COLOR_BUFFED
        elif self.isDebuffed():
            power = COLOR_DAMAGED
        else:
            power = COLOR_WHITE
        
        return (box, power, toughness)
        
    def _constructSurface(self):
        fontName = pygame.font.SysFont('Mono Bold', 30)
        font = pygame.font.SysFont('Mono Bold', 40)

        boxc, pc, tc = self._getColors()

        yh = int(3.0 * self.bb.h / 4.0)
        w1, w2 = int(self.bb.w * 0.25), int(self.bb.w * 0.75)

        box1 = pygame.Rect(0, 0, self.w, self.h)
        box2 = pygame.Rect(0,  yh, w1, self.h - yh)
        box3 = pygame.Rect(w2, yh, w2, self.h - yh)

        self.surface = pygame.Surface(self.bb.size)

        power = font.render(str(self.minion.getPower()), True, pc) 
        toughness = font.render(str(self.minion.getToughness()), True, tc)
        name = fontName.render(str('BANANA'), True, COLOR_WHITE)

        pygame.draw.rect(self.surface, COLOR_WHITE, box2, 2)
        pygame.draw.rect(self.surface, COLOR_WHITE, box3, 2)
        pygame.draw.rect(self.surface, boxc, box1, 2)
        self.surface.blit(name, (4, 4))
        self.surface.blit(power, (4,yh+4))
        self.surface.blit(toughness, (w2+4, yh+4))

    def draw(self, surface):
        super(MinionTemp, self).draw(surface)
        surface.blit(self.surface, self.pos)
    
    """ THESE ARE TEMPORARY MESSAGES THAT WILL BE IMPLEMENTED WITH THE ENGINE"""
    def isDamaged(self):
        return self.minion.damaged
    def isBuffed(self):
        return self.minion.status == 1
    def isDebuffed(self):
        return self.minion.status == -1
    def isTaunt(self):
        return self.minion.taunt
    def isShielded(self):
        return self.minion.shield
    def isOverhealed(self):
        return self.minion.overhealed

class Minion(object):
    """ TODO: THIS IS A TEMPORARY CLASS!!!!"""
    def __init__(self, name, power, toughness):
        self.name = name
        self.power = self.basepower = power
        self.toughness = self.basetoughness = toughness

        self.damaged = False 
        self.status = 0
        self.overhealed = False
        self.shielded = False
        self.taunt = False
        self.stealth = False

    def damage(self, amt):
        if self.shielded:
            self.shielded = False
            return True
        self.toughness -= amt
        self.overhealed = self.basetoughness < self.toughness
        self.damaged = self.basetoughness > self.toughness
        return self.toughness <= 0 

    def heal(self, amt):
        self.toughness += amt
        self.overhealed = self.toughness > self.basetoughness

    def buff(self, pamt, tamt):
        self.heal(tamt)
        self.power += pamt

        self.status = 1

         

    def shield(self):
        self.shielded = True

    def unshield(self):
        self.shielded = False

    def taunt(self):
        self.taunt = True

    def untaunt(self):
        self.taunt = False

    def stealth(self):
        self.stealth = True
        
    def unstealth(self):
        self.stealth = False
    
    def getPower(self):
        return self.power

    def getToughness(self):
        return self.toughness


