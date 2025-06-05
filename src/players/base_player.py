from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Union

from src.action import Action
from src.card import Card
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game import GameState


class BasePlayer(ABC):
    N_CARDS_IN_HAND = 8

    def __init__(self):
        self.hand = list()

    def empty_hand(self):
        self.hand = list()

    def push_hand(self, card: Union[Card, list[Card]]):
        if isinstance(card, Card):
            self.hand.append(card)
        elif isinstance(card, list):
            self.hand.extend(card)
        else:
            raise TypeError

    def pop_hand(self, card: Card):
        self.hand.remove(card)

    def validate_hand_size(self):
        if len(self.hand) != self.N_CARDS_IN_HAND:
            raise HandOverflow(f"Expected size: {self.N_CARDS_IN_HAND}, current hand size: {len(self.hand)}")

    @abstractmethod
    def choose_action(self, game_state: GameState) -> Action:
        pass

    def end_game(self, game_state: GameState):
        """
        This function called in the end of the game and can be used for RL agent
        """

    def end_turn(self, game_state: GameState):
        """
        This function called in the end of the turn and can be used for RL agent
        """


class HandOverflow(Exception):
    pass
