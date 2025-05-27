"""Game engine."""

from __future__ import annotations
from time import sleep
from connect4.const import (
    HEADER_CONTENT,
    OVER_MESSAGE_CONTENT,
    PLAYER_ICONS,
    BUTTON_ARROW,
)
from connect4.types import BoardType, Player
from .state import GameState
from IPython.display import display, clear_output
import ipywidgets as widgets


class Connect4GameEngine:
    """The game engine."""

    def __init__(self, board: BoardType, player0: Player, player1: Player):
        """Initialize."""
        self._rows = len(board.grid)
        self._columns = len(board.grid[0])

        self._log_output = widgets.Output()
        self._ui_output = widgets.Output()

        self._state = GameState(
            board=board, players=(player0, player1), current_player=0
        )
        self._buttons = [
            widgets.Button(
                description=BUTTON_ARROW, layout=widgets.Layout(width="fit-content")
            )
            for _ in range(self._columns)
        ]

        for i, button in enumerate(self._buttons):
            button.on_click(lambda _, i=i: self._move(self._current_player, i))

    def start(self) -> None:
        """Start the game."""
        self._render()

        display(self._log_output)
        display(self._ui_output)

        try:
            self._next_move()
        except KeyboardInterrupt:
            pass  # ignore to allow stopping of AI vs. AI game

    @property
    def _current_player(self) -> Player:
        """The currently active player."""
        return self._state.players[self._state.current_player]

    def _move(self, player: Player, column: int) -> None:
        """
        Make a move as the given player in the given column.

        :param player: The player who makes a move.
        :param column: The index of the column he makes a move in.
        :raises ValueError: If the move is impossible or the game is already over.
        """
        self._state = self._state.move(player, column)

        self._render()
        self._next_move()

    def _next_move(self) -> None:
        """Run the next move."""
        if not self._state.game_over and (next_move := self._current_player.next_move):
            # If the students solution is too fast, we get race conditions when updating the ui
            # via the Jupyter server, so we purposefully make the move calculation slower
            sleep(2)

            with self._log_output:
                column = next_move(
                    self._state.board,
                    self._current_player,
                    self._state.players[(self._state.current_player + 1) % 2]
                )

            self._move(self._current_player, column)

    def _render(self) -> None:
        """Renders the current game state."""
        with self._ui_output:
            clear_output(wait=True)

            player0, player1 = self._state.players
            player0_icon, player1_icon = PLAYER_ICONS

            over_message = ""

            if self._state.game_over:
                if self._state.winner:
                    over_text = f"{self._state.winner.name} wins!"
                else:
                    over_text = "It's a draw!"

                over_message = OVER_MESSAGE_CONTENT.format(text=over_text)

            display(
                widgets.HTML(
                    HEADER_CONTENT.format(
                        over_message=over_message,
                        player0_name=player0.name,
                        player0_icon=player0_icon,
                        player1_name=player1.name,
                        player1_icon=player1_icon,
                        turn=self._current_player.name,
                    )
                )
            )

            grid = widgets.GridspecLayout(
                n_rows=self._rows + 1, n_columns=self._columns, width="fit-content"
            )

            for button_index, button in enumerate(self._buttons):
                button.disabled = bool(
                    self._state.game_over or self._current_player.next_move
                )

                grid[0, button_index] = button

            for row_index, row in enumerate(self._state.board.grid):
                for column_index, column in enumerate(row):
                    text = ""

                    if column:
                        if column is player0:
                            text = player0_icon
                        elif column is player1:
                            text = player1_icon

                    grid[row_index + 1, column_index] = widgets.HTML(
                        f"<div style='text-align: center'>{text}</div>"
                    )

            display(grid)
