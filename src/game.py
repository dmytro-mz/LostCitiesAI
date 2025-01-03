from src.deck import Deck
from src.player import Player
from card import ColorsPiles


class Game:
    def __init__(self, player_1: Player, player_2: Player):
        self.deck = Deck()
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_piles = ColorsPiles()
        self.player_2_piles = ColorsPiles()
        self.discard_piles = ColorsPiles()
        self.set_init_state()

    def set_init_state(self):
        self.deck.shuffle()
        self.player_1_piles.empty_piles()
        self.player_2_piles.empty_piles()
        self.discard_piles.empty_piles()

        for player in [self.player_1, self.player_2]:
            player.empty_hand()
            player.push_hand(self.deck.give_n_next_cards(player.N_CARDS_IN_HAND))
            player.validate_hand_size()

    def play(self):
        i = 0
        while self.deck.get_deck_size():
            player = self.player_1 if i % 2 == 0 else self.player_2
            action = player.choose_action(self)
            self.validate_action(action, player)
            self.do_action(action, player)
            i += 1
        for player in [self.player_1, self.player_2]:
            player.end_game()

    def validate_action(self, action, player):
        pass  # TODO

    def do_action(self, action, player):
        pass  # TODO
