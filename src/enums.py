from enum import Enum


class Color(Enum):
    RED = 0
    BLUE = 1
    YELLOW = 2
    GREEN = 3
    WHITE = 4


class CardAction(Enum):
    PUSH_OWN_PILE = 1
    PUSH_DISCARD_PILE = 2


class PullingSource(Enum):
    DRAW_PILE = 1
    DISCARD_PILE = 2
