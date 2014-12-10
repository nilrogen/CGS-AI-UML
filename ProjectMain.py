import os
import random
import threading

import pygame
from pygame.locals import *

import util.utilities as util

from ui.application import Application
from ui.uiobjects import tmpCard
from ui.cardobjects import UIHandObject, CardView, UIHero, Battlefield
from ui.mana import ManaRegion
from ui.minion import MinionBase

from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.game_objects import Game, card_lookup, Deck
from hearthbreaker.cards import *


# Constant Values
WINDOW_SIZE = (1900, 1000)

MANA_PLAYER_LOC = (1490, 950)
MANA_OPPONENT_LOC = (0, 0)

PLAYER_HAND_LOC = (410, 780)
OPPONENT_HAND_LOC = (410, 0)

PLAYER_HERO_POWER_LOC = (1700, 700)
OPPONENT_HERO_POWER_LOC = (0, 50)

PLAYER_BF_LOC = (400, 300)
OPPONENT_BF_LOC = (400, 500)

class ProjectApplication(Application):

    def __init__(self, game, windowsize=WINDOW_SIZE): # 1900x1000
        super().__init__(windowsize)
        self.game = game
        player, opp = self.game.players[0], self.game.players[1]

        self.handb = UIHandObject.createDefaultHandRegion(PLAYER_HAND_LOC, player)
        self.handt = UIHandObject.createDefaultHandRegion(OPPONENT_HAND_LOC, opp) 
        self.hands = [self.handt, self.handb]

        self.manaplayer = ManaRegion.createDefaultManaRegion(MANA_PLAYER_LOC, player)
        self.manaopponent = ManaRegion.createDefaultManaRegion(MANA_OPPONENT_LOC, opp)
        self.manabars = [self.manaplayer, self.manaopponent]

        self.hero = UIHero(player, PLAYER_HERO_POWER_LOC)
        self.ophero = UIHero(opp, OPPONENT_HERO_POWER_LOC)

        self.playerbf = Battlefield(PLAYER_BF_LOC, 'tmpbg.png', player)
        self.oppbf = Battlefield(OPPONENT_BF_LOC, 'tmpbg.png', opp)
        self.battlefields = [self.playerbf, self.oppbf]

        self.cardmouseoverview = CardView('tmpbg.png', None, (0, 640))

    def init(self):
        super().init()
        self.game.pre_game()
        self.game.current_player = self.game.players[1]

        
    def HandleMouseEvent(self, event):

        for elm in self.hands:
            if elm.containsPoint(event.pos):
                elm.HandleMouseEvent(event)
                mo = elm.getMousedOverCard()
                if mo is None:
                    self.cardmouseoverview.reset()
                else:
                    self.cardmouseoverview.changeCard(mo)
                return True
        for elm in self.battlefields:
            if elm.containsPoint(event.pos):
                elm.HandleMouseEvent(event)
                mo = elm.getMousedOverCard()
                if mo is None:
                    self.cardmouseoverview.reset()
                else:
                    self.cardmouseoverview.changeCard(mo)
                return True


        if self.hero.heropowerbutton.containsPoint(event.pos):
            self.hero.heropowerbutton.HandleMouseEvent(event)
        else:
            #self.hand.removeMouseOver()
            self.cardmouseoverview.reset()

    def UpdateAll(self):
        for h in self.hands:
            h.forceUpdate()
        for m in self.manabars:
            m.forceUpdate()
        for bf in self.battlefields:
            bf.forceUpdate()

        self.hero.forceUpdate()
        self.ophero.forceUpdate()
        

    def onKeydown(self, event):
        if event.key == K_q:
            self.running = False
        elif event.key == K_SPACE:
            self.game.play_single_turn()
            self.UpdateAll()

    def render(self):
        for h in self.hands:
            h.draw(self._display) 
        for m in self.manabars:
            m.draw(self._display)
        for bf in self.battlefields:
            bf.draw(self._display)

        self.cardmouseoverview.draw(self._display)
        self.hero.draw(self._display)
        self.ophero.draw(self._display)
        pygame.display.flip()

class GameEngineThread(threading.Thread):

    def __init__(self, app, game):
        super().__init__()
        self.game = game
        self.app = app
    
    def run(self):
        self.game.pre_game()
        self.game.current_player = self.game.players[1]

        def gameLoop(app, game):
            game.play_single_turn()
            app.UpdateAll()

        while not self.game.game_ended:
            timer = threading.Timer(1.5, gameLoop, self.app, self.game)
            timer.start()

def load_deck(filename):
    cards = []
    character_class = CHARACTER_CLASS.MAGE

    with open(filename, "r") as deck_file:
        contents = deck_file.read()
        items = contents.splitlines()
        for line in items[0:]:
            parts = line.split(" ", 1)
            count = int(parts[0])
            for i in range(0, count):
                card = card_lookup(parts[1])
                if card.character_class != CHARACTER_CLASS.ALL:
                    character_class = card.character_class
                cards.append(card)

    if len(cards) > 30:
        pass

    return Deck(cards, character_class)
    
if __name__ == '__main__':
    deck1 = load_deck('zoo.hsdeck')
    deck2 = load_deck('zoo.hsdeck')

    game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])

    UIProject = ProjectApplication(game, WINDOW_SIZE)
    Engine = GameEngineThread(UIProject, game)

    #Engine.run()
    print('BLsadlasd')
    UIProject.execute()

