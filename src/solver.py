"""
solver.py - Module thuật toán giải N-Queens
Sử dụng thuật toán Backtracking
"""


class NQueensSolver:
    def __init__(self, n, step_callback=None, stats=None):
        """
        n: kích thước bàn cờ
        step_callback: hàm gọi lại mỗi bước (row, col, action)
            action: 'place', 'conflict', 'backtrack', 'success'
        stats: đối tượng Statistics để lưu thống kê
        """
        self.n = n
        self.board = [-1] * n        # board[row] = col của hậu ở hàng đó
        self.step_callback = step_callback
        self.stats = stats
        self.solutions = []
        self._steps = []             # danh sách các bước để step-by-step
        self._generating = False

    def is_safe(self, row, col):
        """Kiểm tra xem có thể đặt hậu tại (row, col) không"""
        for r in range(row):
            c = self.board[r]
            if c == col:                        # cùng cột
                return False
            if abs(r - row) == abs(c - col):    # cùng đường chéo
                return False
        return True

    def solve(self):
        """Tìm tất cả nghiệm, trả về list các nghiệm"""
        self.solutions = []
        self.board = [-1] * self.n
        if self.stats:
            self.stats.reset()
        self._backtrack(0)
        return self.solutions

    def _backtrack(self, row):
        """Đệ quy đặt hậu từng hàng"""
        if row == self.n:
            # Tìm được một nghiệm
            solution = self.board[:]
            self.solutions.append(solution)
            if self.stats:
                self.stats.add_solution()
            if self.step_callback:
                self.step_callback(row - 1, self.board[row - 1], 'success', self.board[:])
            return

        for col in range(self.n):
            if self.stats:
                self.stats.add_attempt()

            if self.step_callback:
                self.step_callback(row, col, 'try', self.board[:])

            if self.is_safe(row, col):
                self.board[row] = col
                if self.step_callback:
                    self.step_callback(row, col, 'place', self.board[:])
                self._backtrack(row + 1)
                # Backtrack
                self.board[row] = -1
                if self.step_callback:
                    self.step_callback(row, col, 'backtrack', self.board[:])
                if self.stats:
                    self.stats.add_backtrack()
            else:
                if self.step_callback:
                    self.step_callback(row, col, 'conflict', self.board[:])

    # ── Step-by-step mode ──────────────────────────────────────────────
    def generate_steps(self):
        """Sinh ra toàn bộ danh sách bước, dùng cho Step-by-Step mode"""
        self._steps = []
        board = [-1] * self.n

        def record(row, col, action, board_state):
            self._steps.append({
                'row': row,
                'col': col,
                'action': action,
                'board': board_state[:]
            })

        def bt(r, b):
            if r == self.n:
                record(r - 1, b[r - 1], 'success', b)
                return
            for c in range(self.n):
                record(r, c, 'try', b)
                if _is_safe(b, r, c):
                    b[r] = c
                    record(r, c, 'place', b)
                    bt(r + 1, b)
                    b[r] = -1
                    record(r, c, 'backtrack', b)
                else:
                    record(r, c, 'conflict', b)

        def _is_safe(b, row, col):
            for r in range(row):
                c = b[r]
                if c == col or abs(r - row) == abs(c - col):
                    return False
            return True

        bt(0, board)
        return self._steps

