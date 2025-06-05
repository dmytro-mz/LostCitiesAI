import random
from src.card import Card, CARD_VALUES
from src.enums import Color


class Deck:
    def __init__(self):
        self._cards = self._create_cards()
        self._pointer = 0
        self.deck: list[Card] = self._get_shuffled_cards()

    def _create_cards(self) -> tuple[Card, ...]:
        return tuple(Card(color=color, value=value) for color in Color for value in CARD_VALUES)

    def _get_shuffled_cards(self) -> list[Card]:
        return random.sample(self._cards, len(self._cards))

    def shuffle(self):
        self._pointer = 0
        self.deck = self._get_shuffled_cards()

    def give_next_card(self):
        self._check_pointer()
        card = self.deck[self._pointer]
        self._pointer += 1
        return card

    def give_n_next_cards(self, n: int):
        if self._pointer + n - 1 >= len(self._cards):
            self._check_pointer()
            raise ValueError(f"Too many cards requested - {n}")
        cards = self.deck[self._pointer : self._pointer + n]
        self._pointer += n
        return cards

    def _check_pointer(self):
        if self._pointer >= len(self._cards):
            raise DeckEmpty

    def get_deck_size(self) -> int:
        return len(self._cards) - self._pointer


class DeckEmpty(Exception):
    pass
