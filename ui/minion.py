import pygame
from pygame.locals import *

import util.utilities as util
from util.math import *

from ui.uiobjects import *
from ui.mousehandler import *

COLOR_WHITE = (255, 255, 255)
COLOR_DAMAGED = (230, 20, 20)
COLOR_BUFFED = (0, 255, 60)
COLOR_BOX_TAUNT = (133, 133, 133)
COLOR_BOX_SHIELD = (255, 255, 0)
COLOR_AURA_SILENCE = (0, 0, 0)
COLOR_AURA_CAN_ATTACK = (0, 255, 60)

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
            aura = COLOR_BOX_TAUNT
        else:
            aura = COLOR_WHITE

        box = COLOR_AURA_CAN_ATTACK

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
        
        return (aura, box, power, toughness)
        
    def _constructSurface(self):
        self.surface = pygame.Surface(self.bb.size)

        subsurface = pygame.Surface(addRect(self.bb, (0, 0), (-8, -8)).size)
        ssbb = subsurface.get_rect()

        fontName = pygame.font.SysFont('Mono Bold', 25)
        font = pygame.font.SysFont('Mono Bold', 40)

        aurac, boxc, pc, tc = self._getColors()

        yh = int(3.0 * ssbb.h / 4.0)
        w1, w2 = int(ssbb.w * 0.25), int(ssbb.w * 0.75)

        if not (self.isTaunt() or self.isShielded()):
            surroundBox = 3
        else:
            surroundBox = 3

        boxoutline = pygame.Rect(0, 0, ssbb.w, ssbb.h)
        boxpower = pygame.Rect(0,  yh, w1, ssbb.h - yh)
        boxtoughness = pygame.Rect(w2, yh, ssbb.w - w2, ssbb.h - yh)
        boxname = scaleRect(ssbb, (1, 1), (1, .2))


        power = font.render(str(self.minion.getPower()), True, pc) 
        toughness = font.render(str(self.minion.getToughness()), True, tc)
        name = fontName.render(str('PLACEHOLDER'), True, COLOR_WHITE)

        pygame.draw.rect(subsurface, boxc, boxpower, 2)
        pygame.draw.rect(subsurface, boxc, boxtoughness, 2)
        pygame.draw.rect(subsurface, boxc, boxname, 2)
        pygame.draw.rect(subsurface, boxc, boxoutline, surroundBox)
        subsurface.blit(name, centerToRect(name.get_rect(), boxname))
        subsurface.blit(power, centerToRect(power.get_rect(), boxpower))
        subsurface.blit(toughness, centerToRect(toughness.get_rect(), boxtoughness))

        self.surface.fill(aurac)
        self.surface.blit(subsurface, centerToRect(ssbb, self.surface.get_rect()))

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
        return self.minion.shielded
    def isOverhealed(self):
        return self.minion.overhealed

    def buff(self, dp, dt):
        self.minion.buff(dp, dt)
        self.forceUpdate()
    def shield(self):
        self.minion.toggleShield()
        self.forceUpdate()
    def taunt(self):
        self.minion.toggleTaunt()
        self.forceUpdate()



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

    def toggleShield(self):
        self.shielded = not self.shielded

    def toggleTaunt(self):
        self.taunt = not self.taunt

    def toggleStealth(self):
        self.stealth = not self.stealth
        
    def getPower(self):
        return self.power

    def getToughness(self):
        return self.toughness



