from action import Action, CardAction, PullingSource
from game import Game, GameState
from player import Player


class SimplePlayer(Player):
    """
    Put in own pile card with the lowest score if possible.
    Put card with the lowest score in discard pile otherwise.
    Always draw card from common draw pile
    """

    def choose_action(self, game_state: GameState) -> Action:
        first_card = None
        for card in sorted(self.hand, key=lambda _card: _card.value):
            if first_card is None:
                first_card = card
            if game_state.players_piles.is_color_empty(card.color) or (
                game_state.players_piles.get_last_card(card.color).value <= card.value
            ):
                return Action(card, CardAction.PUSH_OWN_PILE, PullingSource.DRAW_PILE)
        return Action(first_card, CardAction.PUSH_DISCARD_PILE, PullingSource.DRAW_PILE)


if __name__ == "__main__":
    player_1 = SimplePlayer()
    player_2 = SimplePlayer()
    game = Game(player_1, player_2)
    game.play()
    # n = 5_000
    # scores_sum = 0.0
    # for i in range(n):
    #     game.set_init_state()
    #     game.play()
    #     scores_sum += game.player_1_piles.get_piles_value()
    #     scores_sum += game.player_2_piles.get_piles_value()
    # print(f"AVG score of {n * 2} games:", scores_sum / n / 2)
    # # AVG score of 10000 games: 2.7354
