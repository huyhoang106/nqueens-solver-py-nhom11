"""
board.py - Module vẽ bàn cờ N-Queens bằng tkinter Canvas
"""
import tkinter as tk


# ── Màu sắc ──────────────────────────────────────────────────────────
COLOR_LIGHT      = "#F0D9B5"   # ô sáng (trắng ngà)
COLOR_DARK       = "#B58863"   # ô tối (nâu)
COLOR_QUEEN      = "#27AE60"   # hậu đặt thành công - xanh lá
COLOR_CONFLICT   = "#E74C3C"   # xung đột - đỏ
COLOR_BACKTRACK  = "#F39C12"   # backtrack - vàng cam
COLOR_TRY        = "#3498DB"   # đang thử - xanh dương nhạt
COLOR_SUCCESS    = "#2ECC71"   # nghiệm - xanh sáng
COLOR_TEXT_QUEEN = "#FFFFFF"   # chữ hậu
QUEEN_SYMBOL     = "♛"


class BoardCanvas(tk.Canvas):
    """
    Widget Canvas hiển thị bàn cờ N-Queens.
    Hỗ trợ highlight các ô theo trạng thái thuật toán.
    """

    def __init__(self, parent, n=8, cell_size=60, **kwargs):
        self.n = n
        self.cell_size = cell_size
        size = n * cell_size
        super().__init__(parent, width=size, height=size,
                         bg="#1E1E2E", highlightthickness=2,
                         highlightbackground="#444466", **kwargs)
        self.board = [-1] * n         # board[row] = col
        self.highlights = {}          # (row, col) -> color override
        self._draw_board()

    # ── Public API ────────────────────────────────────────────────────
    def set_n(self, n, cell_size=None):
        """Đặt lại kích thước N và vẽ lại bàn cờ."""
        self.n = n
        if cell_size:
            self.cell_size = cell_size
        else:
            # Tự điều chỉnh cell_size theo N
            self.cell_size = max(36, min(70, 560 // n))
        size = n * self.cell_size
        self.config(width=size, height=size)
        self.reset()

    def reset(self):
        """Xóa tất cả hậu và highlight."""
        self.board = [-1] * self.n
        self.highlights = {}
        self._draw_board()

    def update_board(self, board, highlights=None):
        """
        Cập nhật trạng thái bàn cờ.
        board: list độ dài N, board[row] = col (-1 nếu trống)
        highlights: dict {(row,col): 'conflict'/'backtrack'/'try'/'success'}
        """
        self.board = board[:]
        self.highlights = highlights or {}
        self._draw_board()

    def highlight_cell(self, row, col, state):
        """Highlight một ô cụ thể."""
        self.highlights[(row, col)] = state
        self._draw_cell(row, col)

    def clear_highlights(self):
        self.highlights = {}
        self._draw_board()

    def show_step(self, row, col, action, board):
        """
        Hiển thị một bước của thuật toán.
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
            # highlight ô đang xung đột với hậu nào?
            self._mark_conflicts(row, col, board)
        elif action == 'backtrack':
            self.highlights[(row, col)] = 'backtrack'
        elif action == 'success':
            for r in range(self.n):
                if board[r] != -1:
                    self.highlights[(r, board[r])] = 'success'

        self._draw_board()

    # ── Nội bộ ───────────────────────────────────────────────────────
    def _mark_conflicts(self, row, col, board):
        """Đánh dấu đỏ những ô đang tấn công (row, col)."""
        for r in range(row):
            c = board[r]
            if c == -1:
                continue
            if c == col or abs(r - row) == abs(c - col):
                self.highlights[(r, c)] = 'conflict'

    def _base_color(self, row, col):
        """Màu nền mặc định của ô (sáng/tối xen kẽ)."""
        return COLOR_LIGHT if (row + col) % 2 == 0 else COLOR_DARK

    def _state_color(self, row, col):
        """Màu theo trạng thái highlight."""
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

        # Xóa vùng cũ
        self.delete(f"cell_{row}_{col}")

        # Vẽ ô
        self.create_rectangle(x1, y1, x2, y2,
                               fill=fill, outline="#2C2C4A", width=1,
                               tags=(f"cell_{row}_{col}", "cell"))

        # Vẽ hậu nếu có
        if self.board[row] == col:
            state = self.highlights.get((row, col))
            queen_color = COLOR_TEXT_QUEEN
            font_size = max(14, cs // 2)
            self.create_text(x1 + cs // 2, y1 + cs // 2,
                             text=QUEEN_SYMBOL,
                             fill=queen_color,
                             font=("Segoe UI Symbol", font_size, "bold"),
                             tags=(f"cell_{row}_{col}", "queen"))

    def _draw_board(self):
        self.delete("all")
        for row in range(self.n):
            for col in range(self.n):
                self._draw_cell(row, col)
        # Viền ngoài
        size = self.n * self.cell_size
        self.create_rectangle(0, 0, size, size,
                               outline="#7070A0", width=2, tags="border")
