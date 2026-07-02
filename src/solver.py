"""
solver.py - N-Queens solving algorithm module.

Implements the Backtracking algorithm to find all valid
solutions to the N-Queens problem.
"""


class NQueensSolver:
    def __init__(self, n, step_callback=None, stats=None):
        """
        Initialize the N-Queens solver.

        Args:
            n (int):
                Size of the chessboard (N × N).

            step_callback (callable, optional):
                Callback function invoked after each algorithm step.

                Parameters:
                    row (int)
                    col (int)
                    action (str)

                Supported actions:
                    - 'try'
                    - 'place'
                    - 'conflict'
                    - 'backtrack'
                    - 'success'

            stats (Statistics, optional):
                Statistics object used to record solver performance.
        """
        self.n = n
        self.board = [-1] * n        # board[row] stores the queen's column position
        self.step_callback = step_callback
        self.stats = stats
        self.solutions = []
        self._steps = []             # Stores all recorded steps for step-by-step visualization
        self._generating = False

    def is_safe(self, row, col):
        """
        Determine whether a queen can be safely placed
        at the specified position.
        """
        for r in range(row):
            c = self.board[r]

            # Same column
            if c == col:
                return False

            # Same diagonal
            if abs(r - row) == abs(c - col):
                return False

        return True

    def solve(self):
        """
        Find all valid solutions.

        Returns:
            list: A list containing all discovered solutions.
        """
        self.solutions = []
        self.board = [-1] * self.n

        if self.stats:
            self.stats.reset()

        self._backtrack(0)

        return self.solutions

    def _backtrack(self, row):
        """
        Recursively place queens row by row using
        the Backtracking algorithm.
        """
        if row == self.n:
            # A complete solution has been found
            solution = self.board[:]
            self.solutions.append(solution)

            if self.stats:
                self.stats.add_solution()

            if self.step_callback:
                self.step_callback(
                    row - 1,
                    self.board[row - 1],
                    'success',
                    self.board[:]
                )

            return

        for col in range(self.n):

            if self.stats:
                self.stats.add_attempt()

            if self.step_callback:
                self.step_callback(
                    row,
                    col,
                    'try',
                    self.board[:]
                )

            if self.is_safe(row, col):

                # Place the queen
                self.board[row] = col

                if self.step_callback:
                    self.step_callback(
                        row,
                        col,
                        'place',
                        self.board[:]
                    )

                self._backtrack(row + 1)

                # Remove the queen (Backtracking)
                self.board[row] = -1

                if self.step_callback:
                    self.step_callback(
                        row,
                        col,
                        'backtrack',
                        self.board[:]
                    )

                if self.stats:
                    self.stats.add_backtrack()

            else:
                if self.step_callback:
                    self.step_callback(
                        row,
                        col,
                        'conflict',
                        self.board[:]
                    )

    # ── Step-by-Step Visualization ───────────────────────────────────
    def generate_steps(self):
        """
        Generate every algorithm step for
        step-by-step visualization.
        """
        self._steps = []

        board = [-1] * self.n

        def record(row, col, action, board_state):
            """
            Record one visualization step.
            """
            self._steps.append({
                'row': row,
                'col': col,
                'action': action,
                'board': board_state[:]
            })

        def bt(r, b):
            """
            Recursive backtracking used to
            generate visualization steps.
            """
            if r == self.n:
                record(r - 1, b[r - 1], 'success', b)
                return

            for c in range(self.n):

                # Try placing a queen
                record(r, c, 'try', b)

                if _is_safe(b, r, c):

                    # Place the queen
                    b[r] = c
                    record(r, c, 'place', b)

                    bt(r + 1, b)

                    # Remove the queen (Backtracking)
                    b[r] = -1
                    record(r, c, 'backtrack', b)

                else:
                    # Current position is invalid
                    record(r, c, 'conflict', b)

        def _is_safe(b, row, col):
            """
            Check whether the current position
            is safe on the temporary board.
            """
            for r in range(row):
                c = b[r]

                if c == col or abs(r - row) == abs(c - col):
                    return False

            return True

        bt(0, board)

        return self._steps
