from src.action import Action, CardAction, PullingSource
from src.game import Game
from src.player import Player


class SimplePlayer(Player):
    """
    Iterate through cards ordered by value and perform first available action.
    """
    def choose_action(self, game_state: Game) -> Action:
        for card in sorted(self.hand, key=lambda _card: _card.value):
            my_pile = game_state.player_1_piles if self is game_state.player_1 else game_state.player_2_piles
            if my_pile.is_color_empty(card.color) or (my_pile.get_last_card(card.color).value <= card.value):
                return Action(card, CardAction.PUSH_OWN_PILE, PullingSource.DRAW_PILE)
        return Action(card, CardAction.PUSH_DISCARD_PILE, PullingSource.DRAW_PILE)


if __name__ == "__main__":
    player_1 = SimplePlayer()
    player_2 = SimplePlayer()
    game = Game(player_1, player_2)
    game.play()
