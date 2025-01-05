from dataclasses import dataclass
from src.enums import CardAction, PullingSource

from src.card import Card, Color


@dataclass
class Action:
    card: Card
    card_action: CardAction
    pulling_source: PullingSource
    pulling_color: Color = None

    def __post_init__(self):
        if self.pulling_source == PullingSource.DISCARD_PILE and self.pulling_color is None:
            raise ValueError("PULLING_COLOR has to be provided, if pulling source is discard pile.")
