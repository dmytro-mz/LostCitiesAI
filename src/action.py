from dataclasses import dataclass
from src.enums import PullingSource
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.enums import CardAction
    from src.card import Card
    from src.enums import Color


@dataclass
class Action:
    """
    Action to be performed by a player.
    """

    card: "Card"
    card_action: "CardAction"
    pulling_source: PullingSource
    pulling_color: "Color" = None

    def __post_init__(self):
        if self.pulling_source == PullingSource.DISCARD_PILE and self.pulling_color is None:
            raise ValueError("PULLING_COLOR has to be provided, if pulling source is discard pile.")
