import pygame
from pygame.locals import *

# Hearthbreaker call TODO: Possible change to import 
import hearthbreaker.game_objects

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
COLOR_AURA_FROZEN = (0, 20, 255)

class MinionBase(UISurfaceObject):
    def __init__(self, bb, minion):
        super(MinionBase, self).__init__(bb)
        self.minion = minion
   
class MinionTemp(MinionBase, MouseEventHandler):

    @staticmethod
    def create(minion, bb):
        return MinionTemp(bb, minion.card.name, minion)
    def __init__(self, bb, name, minion):
        super(MinionTemp, self).__init__(bb, minion)

        # Minion Properties
        self.name = name

        if minion is not None:
            self.minion = minion
            self.attack = minion.attack
            self.health = minion.health

    def _getColors(self):
        if self.hasTaunt():
            aura = COLOR_BOX_TAUNT
        else:
            aura = COLOR_WHITE

        box = COLOR_AURA_CAN_ATTACK

        if  self.isDamaged():
            toughness = COLOR_DAMAGED
        elif self.isBuffed():
            toughness = COLOR_BUFFED
        else:
            toughness = COLOR_WHITE

        if self.isBuffed():
            power = COLOR_BUFFED
        elif self.isDamaged():
            power = COLOR_DAMAGED
        else:
            power = COLOR_WHITE
        
        return (aura, box, power, toughness)
        
    def _constructSurface(self):
        self.surface = pygame.Surface(self.bb.size)

        subsurface = pygame.Surface(addRect(self.bb, (0, 0), (-10, -10)).size)
        ssbb = subsurface.get_rect()

        fontName = pygame.font.SysFont('Mono Bold', 25)
        fontText = pygame.font.SysFont('Mono Bold', 40)

        aurac, boxc, pc, tc = self._getColors()

        yh = int(3.0 * ssbb.h / 4.0)
        w1, w2 = int(ssbb.w * 0.25), int(ssbb.w * 0.75)

        boxoutline = pygame.Rect(0, 0, ssbb.w, ssbb.h)
        boxattack = pygame.Rect(0,  yh, w1, ssbb.h - yh)
        boxhealth = pygame.Rect(w2, yh, ssbb.w - w2, ssbb.h - yh)
        boxname = scaleRect(ssbb, (1, 1), (1, .2))

        if self.canAttack():
            attackStr = 'Can Attack'
        else:
            attackStr = 'Can\'t Attack'


        attack = fontText.render(str(self.getAttack()), True, pc) 
        health = fontText.render(str(self.getHealth()), True, tc)
        name = fontName.render(self.name, True, COLOR_WHITE)
        attackStatus = fontName.render(attackStr, True, COLOR_WHITE)


        pygame.draw.rect(subsurface, boxc, boxattack, 2)
        pygame.draw.rect(subsurface, boxc, boxhealth, 2)
        pygame.draw.rect(subsurface, boxc, boxname, 2)
        pygame.draw.rect(subsurface, boxc, boxoutline, 3)

        subsurface.blit(name, centerToRect(name.get_rect(), boxname))
        subsurface.blit(attack, centerToRect(attack.get_rect(), boxattack))
        subsurface.blit(health, centerToRect(health.get_rect(), boxhealth))
        subsurface.blit(attackStatus, centerToRect(attackStatus.get_rect(), ssbb))


        self.surface.fill(aurac)
        self.surface.blit(subsurface, centerToRect(ssbb, self.surface.get_rect()))

    def draw(self, surface):
        super(MinionTemp, self).draw(surface)
        surface.blit(self.surface, self.pos)
    
    """ THESE ARE TEMPORARY MESSAGES THAT WILL BE IMPLEMENTED WITH THE ENGINE"""
    def getHealth(self):
        return self.minion.health
    def getAttack(self):
        return self.minion.calculate_attack()

    def isFrozen(self):
        return self.minion.taunt 
    def hasStealth(self):
        return self.minion.stealth
    def hasTaunt(self):
        return self.minion.taunt
    def hasDivineShield(self):
        return self.minion.divine_shield
    def canAttack(self):
        return self.minion.can_attack
    def isBuffed(self):
        tm = self.minion
        return  tm.attack_delta > 0 and tm.health_delta > 0
    def isDamaged(self):
        tm = self.minion
        return tm.health < tm.base_health

    def damage(self, amt):
        self.minion.damage(amt, None)
        self.forceUpdate()

    def shield(self):
        self.minion.divine_shield = True
