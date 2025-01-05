from enum import Enum


class Color(Enum):
    RED = "Red"
    BLUE = "Blue"
    YELLOW = "Yellow"
    GREEN = "Green"
    WHITE = "White"


class CardAction(Enum):
    PUSH_OWN_PILE = 1
    PUSH_DISCARD_PILE = 2


class PullingSource(Enum):
    DRAW_PILE = 1
    DISCARD_PILE = 2
