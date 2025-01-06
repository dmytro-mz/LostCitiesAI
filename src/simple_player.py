from action import Action, CardAction, PullingSource
from game import Game
from player import Player


class SimplePlayer(Player):
    """
    Put in own pile card with the lowest score if possible.
    Put card with the lowest score in discard pile otherwise.
    Always draw card from common draw pile
    """

    def choose_action(self, game_state: Game) -> Action:
        my_pile = game_state.player_1_piles if self is game_state.player_1 else game_state.player_2_piles
        first_card = None
        for card in sorted(self.hand, key=lambda _card: _card.value):
            if first_card is None:
                first_card = card
            if my_pile.is_color_empty(card.color) or (my_pile.get_last_card(card.color).value <= card.value):
                return Action(card, CardAction.PUSH_OWN_PILE, PullingSource.DRAW_PILE)
        return Action(first_card, CardAction.PUSH_DISCARD_PILE, PullingSource.DRAW_PILE)


if __name__ == "__main__":
    player_1 = SimplePlayer()
    player_2 = SimplePlayer()
    game = Game(player_1, player_2)
    game.play()
