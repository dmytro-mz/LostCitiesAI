import numpy as np

from src.action import Action
from src.game import Game, GameState
from src.players.base_player import BasePlayer
from src.enums import CardAction, PullingSource, Color


class RandomPlayer(BasePlayer):
    """
    Choose random action with uniform distribution
    """

    def choose_action(self, game_state: GameState) -> Action:
        own_possible_cards = []
        for card in self.hand:
            if game_state.players_piles.is_color_empty(card.color) or (
                game_state.players_piles.get_last_card(card.color).value <= card.value
            ):
                own_possible_cards.append(card)
        card_action = np.random.randint(0, self.N_CARDS_IN_HAND + len(own_possible_cards))
        if card_action < self.N_CARDS_IN_HAND:
            card = self.hand[card_action]
            action = CardAction.PUSH_DISCARD_PILE
        else:
            card = own_possible_cards[card_action - self.N_CARDS_IN_HAND]
            action = CardAction.PUSH_OWN_PILE

        possible_colors_to_draw = [
            color
            for color in Color
            if (
                not game_state.discard_piles.is_color_empty(color)
                and (action is CardAction.PUSH_OWN_PILE or color is not card.color)
            )
        ]
        draw_action = np.random.randint(0, len(possible_colors_to_draw) + 1)
        if draw_action == len(possible_colors_to_draw):
            draw_source = PullingSource.DRAW_PILE
            draw_color = None
        else:
            draw_source = PullingSource.DISCARD_PILE
            draw_color = possible_colors_to_draw[draw_action]

        return Action(card, action, draw_source, draw_color)


if __name__ == "__main__":
    player_1 = RandomPlayer()
    player_2 = RandomPlayer()
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
    # # AVG score of 10000 games: -35.5099
