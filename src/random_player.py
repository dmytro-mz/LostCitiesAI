import random

from action import Action
from game import Game
from player import Player
from enums import CardAction, PullingSource, Color


class RandomPlayer(Player):
    """
    Choose random action with uniform distribution
    """

    def choose_action(self, game_state: Game) -> Action:
        my_pile = game_state.player_1_piles if self is game_state.player_1 else game_state.player_2_piles

        own_possible_cards = []
        for card in self.hand:
            if my_pile.is_color_empty(card.color) or (my_pile.get_last_card(card.color).value <= card.value):
                own_possible_cards.append(card)
        card_action = random.randint(0, self.N_CARDS_IN_HAND - 1 + len(own_possible_cards))
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
        draw_action = random.randint(0, len(possible_colors_to_draw))
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
