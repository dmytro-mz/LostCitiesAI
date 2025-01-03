import random
from src.card import Card, Color

class Deck:
    # (0) represents 3 investment cards
    VALUES = [0] * 3 + list(range(2, 11))

    def __init__(self):
        self._cards = self._create_cards()
        self._pointer = 0
        self.deck = self.shuffle()

    def _create_cards(self) -> set[Card]:
        return {
            Card(color=color, value=value)
            for color in Color
            for value in self.VALUES
        }

    def shuffle(self) -> list[Card]:
        self._pointer = 0
        return random.sample(self._cards, len(self._cards))

    def give_next_card(self):
        self._check_pointer()
        card = self._cards[self._pointer]
        self._pointer += 1
        return card

    def give_n_next_cards(self, n: int):
        if self._pointer + n - 1 >= len(self._cards):
            self._check_pointer()
            raise ValueError(f"Too many cards requested - {n}")
        cards = self._cards[self._pointer:self._pointer + n]
        self._pointer += n
        return cards

    def _check_pointer(self):
        if self._pointer >= len(self._cards):
            raise DeckEmpty

    def get_deck_size(self) -> int:
        return len(self._cards) - self._pointer


class DeckEmpty(Exception):
    pass
