from enum import IntEnum


class Color(IntEnum):
    RED = 0
    BLUE = 1
    YELLOW = 2
    GREEN = 3
    WHITE = 4


class CardAction(IntEnum):
    PUSH_OWN_PILE = 1
    PUSH_DISCARD_PILE = 2


class PullingSource(IntEnum):
    DRAW_PILE = 1
    DISCARD_PILE = 2
