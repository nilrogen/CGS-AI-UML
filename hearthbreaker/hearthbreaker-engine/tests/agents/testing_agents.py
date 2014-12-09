import copy
from hearthbreaker.agents.basic_agents import DoNothingAgent


class SpellTestingAgent(DoNothingAgent):
    def __init__(self, play_on=1):
        super().__init__()

        self.player = None

    def do_turn(self, player):

        self.player = player
        while len(player.hand) > 0 and player.hand[0].can_use(player, player.game):
            player.game.play_card(player.hand[0])


class SelfSpellTestingAgent(SpellTestingAgent):
    def __init__(self):
        super().__init__()

    def choose_target(self, targets):
        return self.player.game.current_player.hero


class EnemySpellTestingAgent(SpellTestingAgent):
    def __init__(self):
        super().__init__()

    def choose_target(self, targets):
        return self.player.game.other_player.hero


class EnemyMinionSpellTestingAgent(SpellTestingAgent):
    def __init__(self):
        super().__init__()

    def choose_target(self, targets):
        return self.player.game.other_player.minions[0]


class OneCardPlayingAgent(DoNothingAgent):
    def __init__(self):
        super().__init__()

    def do_turn(self, player):
        if len(player.hand) > 0 and player.hand[0].can_use(player, player.game):
            if player.hand[0].name == "The Coin":
                player.game.play_card(player.hand[0])
            player.game.play_card(player.hand[0])


class MinionAttackingAgent(OneCardPlayingAgent):
    def do_turn(self, player):
        super().do_turn(player)
        for minion in copy.copy(player.minions):
            if minion.can_attack():
                minion.attack()


class WeaponTestingAgent(DoNothingAgent):
    def __init__(self):
        super().__init__()
        self.played_card = False

    def do_turn(self, player):
        if not self.played_card and player.hand[0].can_use(player, player.game):
            player.game.play_card(player.hand[0])
            self.played_card = True

        if player.hero.can_attack():
            player.hero.attack()


class PlayAndAttackAgent(DoNothingAgent):
    def do_turn(self, player):

        while len(player.hand) > 0 and player.hand[0].can_use(player, player.game):
            player.game.play_card(player.hand[0])

        while player.hero.can_attack():
            player.hero.attack()

        done_something = True
        while done_something:
            done_something = False
            for minion in player.minions:
                if minion.can_attack():
                    done_something = True
                    minion.attack()
                    break
