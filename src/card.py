from enum import Enum
from dataclasses import dataclass


class Color(Enum):
    RED = "Red"
    BLUE = "Blue"
    YELLOW = "Yellow"
    GREEN = "Green"
    WHITE = "White"


@dataclass
class Card:
    color: Color
    value: int


class ColorsPiles:
    def __init__(self):
        self.piles: dict[Color, list] = {
            color: list()
            for color in Color
        }

    def empty_piles(self):
        self.piles: dict[Color, list] = {
            color: list()
            for color in Color
        }

    def push(self, card: Card):
        self.piles[card.color].append(card)

    def pop(self, color: Color) -> Card:
        return self.piles[color].pop()

    def is_color_empty(self, color: Color) -> bool:
        return not self.piles[color]
