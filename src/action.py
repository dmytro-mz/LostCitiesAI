from dataclasses import dataclass
from enum import Enum

from src.card import Card, Color


class CardAction(Enum):
    PUSH_OWN_PILE = 1
    PUSH_DISCARD_PILE = 2


class PullingSource(Enum):
    DRAW_PILE = 1
    DISCARD_PILE = 2


@dataclass
class Action:
    card: Card
    card_action: CardAction
    pulling_source: PullingSource
    pulling_color: Color = None

    def __post_init__(self):
        if self.pulling_source == PullingSource.DISCARD_PILE and self.pulling_color is None:
            raise ValueError("PULLING_COLOR has to be provided, if pulling source is discard pile.")
