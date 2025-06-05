from typing import Optional

from src.enums import Color
from dataclasses import dataclass

# (0) represents 3 investment cards
CARD_VALUES = [0] * 3 + list(range(2, 11))


@dataclass
class Card:
    color: Color
    value: int

    def __hash__(self) -> int:
        return hash((self.color, self.value))

    def __eq__(self, other) -> bool:
        if self.color == other.color and self.value == other.value:
            return True
        return False


class ColorsPiles:
    def __init__(self):
        self.piles: dict[Color, list] = {color: list() for color in Color}

    def empty_piles(self):
        self.piles: dict[Color, list] = {color: list() for color in Color}

    def push(self, card: Card):
        self.piles[card.color].append(card)

    def pop(self, color: Color) -> Card:
        return self.piles[color].pop()

    def is_color_empty(self, color: Color) -> bool:
        return not self.piles[color]

    def get_last_card(self, color: Color) -> Optional[Card]:
        if self.is_color_empty(color):
            return None
        return self.piles[color][-1]

    def get_piles_value(self) -> int:
        return sum([self.get_pile_value(color) for color in Color])

    def get_pile_value(self, color: Color) -> int:
        if self.is_color_empty(color):
            return 0
        value = sum([card.value for card in self.piles[color]])
        value -= 20
        value *= len([1 for card in self.piles[color] if card.value == 0]) + 1
        if len(self.piles[color]) >= 8:
            value += 20
        return value
