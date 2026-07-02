"""
board.py - Module for drawing the N-Queens chessboard using tkinter Canvas.
"""
import tkinter as tk


# ── Color definitions ────────────────────────────────────────────────
COLOR_LIGHT      = "#F0D9B5"   # Light square (ivory)
COLOR_DARK       = "#B58863"   # Dark square (brown)
COLOR_QUEEN      = "#27AE60"   # Successfully placed queen (green)
COLOR_CONFLICT   = "#E74C3C"   # Conflict (red)
COLOR_BACKTRACK  = "#F39C12"   # Backtracking (orange)
COLOR_TRY        = "#3498DB"   # Current trial (light blue)
COLOR_SUCCESS    = "#2ECC71"   # Final solution (bright green)
COLOR_TEXT_QUEEN = "#FFFFFF"   # Queen symbol color
QUEEN_SYMBOL     = "♛"


class BoardCanvas(tk.Canvas):
    """
    Canvas widget for displaying the N-Queens chessboard.
    Supports highlighting cells according to the algorithm state.
    """

    def __init__(self, parent, n=8, cell_size=60, **kwargs):
        self.n = n
        self.cell_size = cell_size
        size = n * cell_size
        super().__init__(parent, width=size, height=size,
                         bg="#1E1E2E", highlightthickness=2,
                         highlightbackground="#444466", **kwargs)
        self.board = [-1] * n         # board[row] = col
        self.highlights = {}          # (row, col) -> highlight state
        self._draw_board()

    # ── Public API ────────────────────────────────────────────────────
    def set_n(self, n, cell_size=None):
        """Set a new board size and redraw the chessboard."""
        self.n = n
        if cell_size:
            self.cell_size = cell_size
        else:
            # Automatically adjust the cell size based on N
            self.cell_size = max(36, min(70, 560 // n))
        size = n * self.cell_size
        self.config(width=size, height=size)
        self.reset()

    def reset(self):
        """Clear all queens and highlights."""
        self.board = [-1] * self.n
        self.highlights = {}
        self._draw_board()

    def update_board(self, board, highlights=None):
        """
        Update the board state.

        board: list of length N, where board[row] = col (-1 if empty)
        highlights: dict {(row, col): 'conflict'/'backtrack'/'try'/'success'}
        """
        self.board = board[:]
        self.highlights = highlights or {}
        self._draw_board()

    def highlight_cell(self, row, col, state):
        """Highlight a specific cell."""
        self.highlights[(row, col)] = state
        self._draw_cell(row, col)

    def clear_highlights(self):
        """Remove all highlights."""
        self.highlights = {}
        self._draw_board()

    def show_step(self, row, col, action, board):
        """
        Display one step of the algorithm.

        action: 'try', 'place', 'conflict', 'backtrack', 'success'
        """
        self.board = board[:]
        self.highlights = {}

        if action == 'try':
            self.highlights[(row, col)] = 'try'
        elif action == 'place':
            self.highlights[(row, col)] = 'place'
        elif action == 'conflict':
            self.highlights[(row, col)] = 'conflict'
            # Highlight the queens that are attacking this position
            self._mark_conflicts(row, col, board)
        elif action == 'backtrack':
            self.highlights[(row, col)] = 'backtrack'
        elif action == 'success':
            for r in range(self.n):
                if board[r] != -1:
                    self.highlights[(r, board[r])] = 'success'

        self._draw_board()

    # ── Internal methods ──────────────────────────────────────────────
    def _mark_conflicts(self, row, col, board):
        """Mark all queens attacking (row, col) in red."""
        for r in range(row):
            c = board[r]
            if c == -1:
                continue
            if c == col or abs(r - row) == abs(c - col):
                self.highlights[(r, c)] = 'conflict'

    def _base_color(self, row, col):
        """Return the default background color of a square."""
        return COLOR_LIGHT if (row + col) % 2 == 0 else COLOR_DARK

    def _state_color(self, row, col):
        """Return the color corresponding to the current highlight state."""
        state = self.highlights.get((row, col))
        mapping = {
            'try':       COLOR_TRY,
            'place':     COLOR_QUEEN,
            'conflict':  COLOR_CONFLICT,
            'backtrack': COLOR_BACKTRACK,
            'success':   COLOR_SUCCESS,
        }
        return mapping.get(state, None)

    def _draw_cell(self, row, col):
        cs = self.cell_size
        x1, y1 = col * cs, row * cs
        x2, y2 = x1 + cs, y1 + cs

        fill = self._state_color(row, col) or self._base_color(row, col)

        # Remove the previous drawing of this cell
        self.delete(f"cell_{row}_{col}")

        # Draw the square
        self.create_rectangle(x1, y1, x2, y2,
                              fill=fill, outline="#2C2C4A", width=1,
                              tags=(f"cell_{row}_{col}", "cell"))

        # Draw the queen if present
        if self.board[row] == col:
            queen_color = COLOR_TEXT_QUEEN
            font_size = max(14, cs // 2)
            self.create_text(x1 + cs // 2, y1 + cs // 2,
                             text=QUEEN_SYMBOL,
                             fill=queen_color,
                             font=("Segoe UI Symbol", font_size, "bold"),
                             tags=(f"cell_{row}_{col}", "queen"))

    def _draw_board(self):
        """Redraw the entire chessboard."""
        self.delete("all")
        for row in range(self.n):
            for col in range(self.n):
                self._draw_cell(row, col)

        # Draw the outer border
        size = self.n * self.cell_size
        self.create_rectangle(0, 0, size, size,
                              outline="#7070A0", width=2, tags="border")
