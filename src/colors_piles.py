
from src.enums import Color
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.card import Card


class ColorsPiles:
    def __init__(self):
        self.piles: dict[Color, list["Card"]] = {color: list() for color in Color}

    def empty_piles(self):
        self.piles: dict[Color, list["Card"]] = {color: list() for color in Color}

    def push(self, card: "Card"):
        self.piles[card.color].append(card)

    def pop(self, color: Color) -> "Card":
        return self.piles[color].pop()

    def is_color_empty(self, color: Color) -> bool:
        """
        Check if the pile of the color is empty.
        """
        return not self.piles[color]

    def get_last_card(self, color: Color) -> Optional["Card"]:
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
