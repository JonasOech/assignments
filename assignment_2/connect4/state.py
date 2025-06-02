"""State of a game."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .types import BoardType, Player


@dataclass(frozen=True)
class GameState:
    """The state of a game."""

    board: BoardType
    players: tuple[Player, Player]
    current_player: Literal[0, 1]
    game_over: bool = False
    winner: Player | None = None

    def move(self, player: Player, column: int) -> GameState:
        """
        Make a move as the given player in the given column.

        :param player: The player who makes a move.
        :param column: The index of the column he makes a move in.
        :return state: The resulting state.
        :raises ValueError: If the move is impossible or the game is already over.
        """
        if self.game_over:
            raise ValueError(f"Invalid move from '{player}', the game is already over.")

        if column not in (valid_moves := self.board.valid_moves()):
            raise ValueError(f"Invalid move from '{player}' to column '{column}'.")

        new_board = self.board.drop_in_column(column=column, player=player)
        winner = new_board.get_winner()
        game_over = winner or len(valid_moves) == 1

        return GameState(
            board=new_board,
            players=self.players,
            current_player=(self.current_player + 1) % 2,
            game_over=game_over,
            winner=winner,
        )
