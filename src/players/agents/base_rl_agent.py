from abc import ABC
from typing import Optional

import torch

from src.action import Action
from src.card import Card, CARD_VALUES
from src.enums import Color, PullingSource, CardAction
from src.game import GameState
from src.players.base_player import BasePlayer
import numpy as np

COLOR_COUNT = len(Color)
CARD_VALUES_COUNT = len(set(CARD_VALUES))
MAX_PILE_VALUE = sum(CARD_VALUES) * 4
COMMON_DTYPE = np.float32


class EGreedy:
    def __init__(self, epsilon: float):
        self.epsilon = epsilon

    def choose(self, values: list[float], direction_max=True):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, len(values))
        if direction_max:
            return np.argmax(values)
        return np.argmin(values)


class BaseRLAgent(BasePlayer, ABC):
    ACTION_SPACE_SIZE = BasePlayer.N_CARDS_IN_HAND * 2 * (len(Color) + 1)

    def __init__(
        self,
        train_buffer,
        model: torch.nn.Module,
        epsilon=0.1,
    ):
        super().__init__()
        self.train_buffer = train_buffer
        self.e_greedy = EGreedy(epsilon)
        self.model = model
        self.target_model = type(model)()
        self._copy_weights_to_target_model()
        self._sorted_hand = None
        self._action_list = None
        self._game_train_records = []

    def _copy_weights_to_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()

    def _create_local_state(self):
        self._sorted_hand = self._get_sorted_hand()
        self._action_list = self._get_action_list()

    def _drop_local_state(self):
        self._sorted_hand = None
        self._action_list = None

    def _get_sorted_hand(self) -> list[Card]:
        return sorted(self.hand, key=lambda card: (card.value, card.color.value))

    def _get_action_list(self) -> list[Action]:
        return [
            Action(card, card_action, pulling_source, color)
            for card in self._sorted_hand
            for card_action in CardAction
            for pulling_source, color in (
                [(PullingSource.DRAW_PILE, None)] + [(PullingSource.DISCARD_PILE, c) for c in Color]
            )
        ]

    def _create_observation(self, game_state: GameState):
        """
        Creates observation of the world for agent.
        Contains:
            - Cards is hand
            - Diff in values between own pile top card and cards is hand
            - Can card from hand be played by opponent
            - Top cards in own pile
            - Score of each color in own pile + total score
            - Top cards in opponents pile
            - Score of each color in opponents pile + total score
            - Top cards in discard pile
            - Diff in values between own pile top card and top card from discard pile
            - Size of draw deck
        Don't know how to represent:
            - All cards in piles (onw, opponents and discard)
            - Cards not seen in the game yet
        """
        norm_hand_val_diff_to_own_pile: list[float] = [
            (
                (card.value - self._get_card_value_or_zero(game_state.players_piles.get_last_card(card.color)))
                / max(CARD_VALUES)
            )
            for card in self._sorted_hand
        ]
        can_opponent_play_my_card: list[bool] = [
            card.value >= self._get_card_value_or_zero(game_state.opponents_piles.get_last_card(card.color))
            for card in self._sorted_hand
        ]
        top_cards_in_own_pile: list[Optional[Card]] = [game_state.players_piles.get_last_card(color) for color in Color]
        norm_own_pile_scores: list[float] = [
            game_state.players_piles.get_pile_value(color) / MAX_PILE_VALUE for color in Color
        ]
        norm_total_own_score: float = game_state.players_piles.get_piles_value() / (MAX_PILE_VALUE * COLOR_COUNT)
        top_cards_in_opp_pile: list[Optional[Card]] = [
            game_state.opponents_piles.get_last_card(color) for color in Color
        ]
        norm_opp_pile_scores: list[float] = [
            game_state.opponents_piles.get_pile_value(color) / MAX_PILE_VALUE for color in Color
        ]
        norm_total_opp_score: float = game_state.opponents_piles.get_piles_value() / (MAX_PILE_VALUE * COLOR_COUNT)
        top_cards_in_discard_pile: list[Optional[Card]] = [
            game_state.discard_piles.get_last_card(color) for color in Color
        ]
        norm_discard_pile_val_diff_to_own_pile: list[float] = [
            (
                (
                    self._get_card_value_or_zero(game_state.discard_piles.get_last_card(color))
                    - self._get_card_value_or_zero(game_state.players_piles.get_last_card(color))
                )
                / max(CARD_VALUES)
            )
            for color in Color
        ]
        draw_deck_size = game_state.draw_stack_size / 44  # 44 is size of the deck in the start of the game

        return (
            self._sorted_hand,
            norm_hand_val_diff_to_own_pile,
            can_opponent_play_my_card,
            top_cards_in_own_pile,
            norm_own_pile_scores,
            norm_total_own_score,
            top_cards_in_opp_pile,
            norm_opp_pile_scores,
            norm_total_opp_score,
            top_cards_in_discard_pile,
            norm_discard_pile_val_diff_to_own_pile,
            draw_deck_size,
        )

    def _get_card_value_or_zero(self, card: Card = None) -> float:
        if card is None:
            return 0
        return card.value

    def _get_action_mask(self, game_state: GameState) -> np.ndarray:
        action_mask = np.ones(self.ACTION_SPACE_SIZE)

        for card in self._sorted_hand:
            # disallow discard and draw the same card
            action_mask[
                self._get_action_index(
                    card=card,
                    card_action=CardAction.PUSH_DISCARD_PILE,
                    pulling_source=PullingSource.DISCARD_PILE,
                    color=card.color,
                )
            ] = 0

            # check if card can be pushed to own pile
            if card.value < self._get_card_value_or_zero(game_state.players_piles.get_last_card(card.color)):
                action_mask[
                    self._get_action_index(
                        card=card,
                        card_action=CardAction.PUSH_OWN_PILE,
                    )
                ] = 0

        # check if card can be drawn from discard pile
        for color in Color:
            if game_state.discard_piles.is_color_empty(color):
                action_mask[
                    self._get_action_index(
                        pulling_source=PullingSource.DISCARD_PILE,
                        color=color,
                    )
                ] = 0

        return action_mask

    def _get_action_index(self, card=None, card_action=None, pulling_source=None, color=None) -> list[int]:
        return [
            ind
            for ind, action in enumerate(self._action_list)
            if not (card is not None and action.card is card)
            and not (card_action is not None and action.card_action is card_action)
            and not (pulling_source is not None and action.pulling_source is pulling_source)
            and not (color is not None and action.pulling_color is color)
        ]

    def _get_action_by_index(self, index: int) -> Action:
        return self._action_list[index]

    def _card_ohe_encoder(self, card: Optional[Card]) -> np.ndarray:
        color_one_hot = np.zeros(COLOR_COUNT, dtype=COMMON_DTYPE)
        if card:
            color_one_hot[card.color.value] = 1

        value_one_hot = np.zeros(CARD_VALUES_COUNT, dtype=COMMON_DTYPE)
        if card:
            if card.value == 0:  # Investment card
                value_one_hot[-1] = 1
            else:
                value_one_hot[card.value - 2] = 1

        return np.concatenate([color_one_hot, value_one_hot], dtype=COMMON_DTYPE)
