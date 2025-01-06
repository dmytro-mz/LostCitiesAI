from action import Action, CardAction, PullingSource
from deck import Deck
from player import Player
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
            player.end_game(self)

    def validate_action(self, action: Action, player: Player):
        assert action.card in player.hand
        if action.card_action == CardAction.PUSH_OWN_PILE:
            player_pile = self.player_1_piles if player is self.player_1 else self.player_2_piles
            assert player_pile.is_color_empty(action.card.color) or (
                player_pile.get_last_card(action.card.color).value <= action.card.value
            )
        if action.pulling_source == PullingSource.DISCARD_PILE:
            assert action.pulling_color is not None
            assert not self.discard_piles.is_color_empty(action.pulling_color)

    def do_action(self, action: Action, player: Player):
        player.pop_hand(action.card)

        if action.card_action == CardAction.PUSH_OWN_PILE:
            pile = self.player_1_piles if player is self.player_1 else self.player_2_piles
        elif action.card_action == CardAction.PUSH_DISCARD_PILE:
            pile = self.discard_piles
        else:
            raise NotImplementedError
        pile.push(action.card)

        if action.pulling_source == PullingSource.DISCARD_PILE:
            player.push_hand(self.discard_piles.pop(action.pulling_color))
        elif action.pulling_source == PullingSource.DRAW_PILE:
            player.push_hand(self.deck.give_next_card())
        else:
            raise NotImplementedError

        player.validate_hand_size()
