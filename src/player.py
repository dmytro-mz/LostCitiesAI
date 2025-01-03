from abc import abstractmethod
from typing import Union

from src.action import Action
from src.card import Card
from src.game import Game


class Player:
    N_CARDS_IN_HAND = 8

    def __init__(self):
        self.hand = set()

    def empty_hand(self):
        self.hand = set()

    def push_hand(self, card: Union[Card, list[Card]]):
        if isinstance(card, Card):
            self.hand.add(card)
        elif isinstance(card, list):
            for card in card:
                self.hand.add(card)
        else:
            raise TypeError

    def pop_hand(self, card: Card):
        self.hand.remove(card)

    def validate_hand_size(self):
        if len(self.hand) != self.N_CARDS_IN_HAND:
            raise HandOverflow(f"Expected size: {self.N_CARDS_IN_HAND}, current hand size: {len(self.hand)}")

    @abstractmethod
    def choose_action(self, game_state: Game) -> Action:
        pass

    def end_game(self, game_state: Game):
        """
        This function called in the end of the game and can be used for RL agent
        """
        pass


class HandOverflow(Exception):
    pass