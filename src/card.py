from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.enums import Color


# (0) represents 3 investment cards
CARD_VALUES = [0] * 3 + list(range(2, 11))


@dataclass
class Card:
    color: "Color"
    value: int

    def __hash__(self) -> int:
        return hash((self.color, self.value))

    def __eq__(self, other: "Card") -> bool:
        if self.color == other.color and self.value == other.value:
            return True
        return False
