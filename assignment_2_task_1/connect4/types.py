"""Types."""

from __future__ import annotations
from typing import List, Protocol, Callable, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    """A player who can either be ai-controlled or human controlled."""

    name: str
    next_move: Callable[[BoardType, Player, Player], int] | None

    @staticmethod
    def ai(name: str, move: Callable[[BoardType, Player, Player], int]):
        """
        Create an AI player with the given name and move function.

        :param name: The name of this player.
        :param move: The function that determines the next move.
        :returns Player: The created player.
        """
        return Player(name, move)

    @staticmethod
    def human(name: str):
        """
        Create a human player with the given name.

        :param name: The name of this player.
        :returns Player: The created player.
        """
        return Player(name, next_move=None)


class BoardType(Protocol):
    """Wrapper arround the actual board implementation, used to abstract from the real class."""

    grid: List[List[Optional[Player]]]

    def drop_in_column(self, player: Player, column: int) -> Optional[BoardType]: ...

    def valid_moves(self) -> List[int]: ...

    def get_winner(self) -> Optional[Player]: ...
