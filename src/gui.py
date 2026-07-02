"""
gui.py - Main graphical user interface for the N-Queens Solver
Integrates: Board, Solver, Statistics
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

from board import BoardCanvas
from solver import NQueensSolver
from statistics import Statistics, benchmark


# ── Application theme colors ────────────────────────────────────────────────
BG_MAIN   = "#12121F"
BG_PANEL  = "#1A1A2E"
BG_CARD   = "#22223A"
FG_TEXT   = "#E0E0F0"
FG_DIM    = "#8888AA"
ACCENT    = "#7C6AF7"
ACCENT2   = "#27AE60"
BTN_FG    = "#FFFFFF"

FONT_TITLE  = ("Consolas", 13, "bold")
FONT_LABEL  = ("Consolas", 10)
FONT_STAT   = ("Consolas", 11, "bold")
FONT_BTN    = ("Consolas", 10, "bold")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("N-Queens Solver  ♛")
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)

        # Application state
        self.n_var        = tk.IntVar(value=8)
        self.speed_var    = tk.DoubleVar(value=50)   # ms delay
        self.stats        = Statistics()
        self.solver       = None
        self.steps        = []
        self.step_index   = 0
        self._anim_id     = None
        self._running     = False
        self._step_mode   = False

        self._build_ui()
        self._update_board_size()

    # ════════════════════════════════════════════════════════════════
    # Build UI
    # ════════════════════════════════════════════════════════════════
    def _build_ui(self):
        # ── Main layout ───────────────────────────────────────────
        self.left_panel = tk.Frame(self, bg=BG_PANEL, padx=16, pady=16)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self, bg=BG_MAIN, padx=12, pady=12)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_left_panel()
        self._build_right_panel()

    def _build_left_panel(self):
        p = self.left_panel

        # Title
        tk.Label(p, text="♛ N-Queens", font=("Consolas", 16, "bold"),
                 bg=BG_PANEL, fg=ACCENT).pack(pady=(0, 16))

        # ── N selector ─────────────────────────────────────────────
        card = self._card(p, "Board Size")
        row_n = tk.Frame(card, bg=BG_CARD)
        row_n.pack(fill=tk.X)
        for n in [4, 6, 8, 10, 12]:
            tk.Button(row_n, text=str(n), font=FONT_BTN, width=3,
                      bg="#2A2A4A", fg=FG_TEXT, activebackground=ACCENT,
                      activeforeground=BTN_FG, bd=0, pady=4,
                      command=lambda v=n: self._set_n(v)
                      ).pack(side=tk.LEFT, padx=2, pady=4)

        spin_frame = tk.Frame(card, bg=BG_CARD)
        spin_frame.pack(fill=tk.X, pady=4)
        tk.Label(spin_frame, text="Custom:", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_DIM).pack(side=tk.LEFT)
        self.spin_n = tk.Spinbox(spin_frame, from_=4, to=20, width=4,
                                 textvariable=self.n_var,
                                 font=FONT_LABEL, bg=BG_CARD, fg=FG_TEXT,
                                 buttonbackground=BG_CARD,
                                 command=self._on_spin_n)
        self.spin_n.pack(side=tk.LEFT, padx=6)
        tk.Button(spin_frame, text="✓", font=FONT_BTN,
                  bg=ACCENT, fg=BTN_FG, bd=0, padx=6,
                  command=self._on_spin_n).pack(side=tk.LEFT)

        # ── Buttons ────────────────────────────────────────────────
        card2 = self._card(p, "Controls")

        self.btn_solve = self._btn(card2, "▶  Solve (Animation)",
                                   ACCENT, self._solve_animate)
        self.btn_solve.pack(fill=tk.X, pady=3)

        self.btn_step = self._btn(card2, "→  Next Step",
                                  "#2980B9", self._next_step)
        self.btn_step.pack(fill=tk.X, pady=3)

        self.btn_pause = self._btn(card2, "⏸  Pause / Resume",
                                   "#8E44AD", self._pause_resume)
        self.btn_pause.pack(fill=tk.X, pady=3)

        self.btn_reset = self._btn(card2, "↺  Reset",
                                   "#C0392B", self._reset)
        self.btn_reset.pack(fill=tk.X, pady=3)

        self.btn_bench = self._btn(card2, "📊  Benchmark",
                                   "#16A085", self._run_benchmark)
        self.btn_bench.pack(fill=tk.X, pady=(8, 3))

        # ── Speed ──────────────────────────────────────────────────
        card3 = self._card(p, "Animation Speed")
        speed_row = tk.Frame(card3, bg=BG_CARD)
        speed_row.pack(fill=tk.X)
        tk.Label(speed_row, text="Slow", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_DIM).pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_row, from_=1, to=200,
                                    orient=tk.HORIZONTAL,
                                    variable=self.speed_var,
                                    bg=BG_CARD, fg=FG_TEXT,
                                    troughcolor="#333355",
                                    highlightthickness=0,
                                    showvalue=False, length=130,
                                    command=lambda v: self._on_speed(v))
        self.speed_scale.set(50)
        self.speed_scale.pack(side=tk.LEFT, padx=4)
        tk.Label(speed_row, text="Fast", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_DIM).pack(side=tk.LEFT)

        self.lbl_speed = tk.Label(card3, text="Delay: 150ms",
                                   font=FONT_LABEL, bg=BG_CARD, fg=FG_DIM)
        self.lbl_speed.pack()
        self._on_speed(50)

        # ── Statistics ─────────────────────────────────────────────
        card4 = self._card(p, "Statistics")
        self.lbl_attempts   = self._stat_label(card4, "Attempts",   "0")
        self.lbl_backtracks = self._stat_label(card4, "Backtracks", "0")
        self.lbl_solutions  = self._stat_label(card4, "Solutions",  "0")
        self.lbl_time       = self._stat_label(card4, "Time",       "0.0000s")

        # ── Status ─────────────────────────────────────────────────
        self.lbl_status = tk.Label(p, text="Ready.",
                                   font=FONT_LABEL, bg=BG_PANEL,
                                   fg=ACCENT2, wraplength=220, justify=tk.LEFT)
        self.lbl_status.pack(pady=(12, 0), anchor="w")

    def _build_right_panel(self):
        p = self.right_frame
        # Chessboard title
        self.lbl_board_title = tk.Label(p, text="Chessboard 8×8",
                                         font=FONT_TITLE,
                                         bg=BG_MAIN, fg=FG_TEXT)
        self.lbl_board_title.pack(pady=(0, 8))

        # Board canvas
        self.board_canvas = BoardCanvas(p, n=8, cell_size=60)
        self.board_canvas.pack()

        # Color legend
        legend = tk.Frame(p, bg=BG_MAIN)
        legend.pack(pady=8)
        for color, label in [
            ("#27AE60", "Place Queen"),
            ("#E74C3C", "Conflict"),
            ("#F39C12", "Backtrack"),
            ("#3498DB", "Trying"),
            ("#2ECC71", "Solution"),
        ]:
            fr = tk.Frame(legend, bg=BG_MAIN)
            fr.pack(side=tk.LEFT, padx=6)
            tk.Label(fr, bg=color, width=2, height=1).pack(side=tk.LEFT)
            tk.Label(fr, text=label, font=FONT_LABEL,
                     bg=BG_MAIN, fg=FG_DIM).pack(side=tk.LEFT, padx=2)

    # ════════════════════════════════════════════════════════════════
    # Helper builders
    # ════════════════════════════════════════════════════════════════
    def _card(self, parent, title):
        frame = tk.LabelFrame(parent, text=f"  {title}  ",
                               font=FONT_LABEL,
                               bg=BG_CARD, fg=FG_DIM,
                               labelanchor="nw", bd=1,
                               relief=tk.GROOVE, padx=8, pady=6)
        frame.pack(fill=tk.X, pady=6)
        return frame

    def _btn(self, parent, text, color, cmd):
        return tk.Button(parent, text=text, font=FONT_BTN,
                         bg=color, fg=BTN_FG,
                         activebackground=color, activeforeground=BTN_FG,
                         bd=0, pady=6, cursor="hand2",
                         command=cmd)

    def _stat_label(self, parent, key, value):
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill=tk.X, pady=1)
        tk.Label(row, text=f"{key}:", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_DIM, width=11, anchor="w").pack(side=tk.LEFT)
        lbl = tk.Label(row, text=value, font=FONT_STAT,
                       bg=BG_CARD, fg=FG_TEXT)
        lbl.pack(side=tk.LEFT)
        return lbl

    # ════════════════════════════════════════════════════════════════
    # Actions
    # ════════════════════════════════════════════════════════════════
    def _set_n(self, n):
        self.n_var.set(n)
        self._update_board_size()
        self._reset()

    def _on_spin_n(self):
        try:
            n = int(self.spin_n.get())
            n = max(4, min(20, n))
        except ValueError:
            n = 8
        self.n_var.set(n)
        self._update_board_size()
        self._reset()

    def _update_board_size(self):
        n = self.n_var.get()
        cs = max(32, min(70, 560 // n))
        self.board_canvas.set_n(n, cs)
        self.lbl_board_title.config(text=f"Chessboard {n}×{n}")

    def _on_speed(self, v):
        # Convert slider value (1..200) to animation delay (300ms..1ms)
        v = float(v)
        delay = int(301 - v * 1.5)
        delay = max(1, delay)
        self.speed_var.set(v)
        self.lbl_speed.config(text=f"Delay: {delay}ms")

    def _get_delay(self):
        v = self.speed_var.get()
        return max(1, int(301 - v * 1.5))

    def _reset(self):
        """Stop animation, clear the board, and reset statistics."""
        self._stop_animation()
        self._running = False
        self._step_mode = False
        self.steps = []
        self.step_index = 0
        self.stats.reset()
        self.board_canvas.reset()
        self._update_stats()
        self._status("Ready.")

    def _stop_animation(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
            self._anim_id = None

    # ── Animated Solver ───────────────────────────────────────────
    def _solve_animate(self):
        self._reset()
        n = self.n_var.get()
        self._step_mode = False
        self._running = True

        # Generate solving steps in a background thread to keep the UI responsive
        self._status("Generating solving steps...")
        self.btn_solve.config(state=tk.DISABLED)

        def generate():
            solver = NQueensSolver(n)
            steps = solver.generate_steps()
            self.steps = steps
            self.step_index = 0
            self.stats.start()
            self.after(0, self._anim_start)

        threading.Thread(target=generate, daemon=True).start()

    def _anim_start(self):
        self._status(f"Running animation ({len(self.steps)} steps)...")
        self._anim_tick()

    def _anim_tick(self):
        if not self._running:
            return
        if self.step_index >= len(self.steps):
            self._anim_done()
            return

        step = self.steps[self.step_index]
        self._apply_step(step)
        self._count_step(step)
        self.step_index += 1

        delay = self._get_delay()
        self._anim_id = self.after(delay, self._anim_tick)

    def _anim_done(self):
        self.stats.stop()
        self._running = False
        self.btn_solve.config(state=tk.NORMAL)
        self._status(
            f"✓ Completed! Found {self.stats.solutions} nghiệm "
            f"in {self.stats.runtime_str()}."
        )
        self._update_stats()

    # ── Step-by-Step Execution ──────────────────────────────────────────────
    def _next_step(self):
        if not self.steps:
            # Generate solving steps for the first execution
            n = self.n_var.get()
            self._step_mode = True
            self._running = False
            solver = NQueensSolver(n)
            self.steps = solver.generate_steps()
            self.step_index = 0
            self.stats.reset()
            self.stats.start()
            self._status(f"Step-by-step ({len(self.steps)} steps). Press Next.")

        if self.step_index >= len(self.steps):
            self.stats.stop()
            self._status(f"✓ Completed! {self.stats.solutions} nghiệm.")
            self._update_stats()
            return

        step = self.steps[self.step_index]
        self._apply_step(step)
        self._count_step(step)
        self.step_index += 1
        self._status(
            f"Step {self.step_index}/{len(self.steps)} | "
            f"Row {step['row']}, Column {step['col']} | {step['action']}"
        )
        self._update_stats()

    # ── Pause / Resume ────────────────────────────────────────────
    def _pause_resume(self):
        if self._running:
            self._running = False
            self._stop_animation()
            self._status("⏸ Paused. Press Pause/Resume to continue.")
        else:
            if self.steps and self.step_index < len(self.steps):
                self._running = True
                self._anim_tick()
                self._status("▶ Resuming animation...")

    # ── Apply Step to the Chessboard ──────────────────────────────────────
    def _apply_step(self, step):
        self.board_canvas.show_step(
            step['row'], step['col'], step['action'], step['board']
        )

    def _count_step(self, step):
        action = step['action']
        if action in ('try', 'place', 'conflict'):
            self.stats.add_attempt()
        if action == 'backtrack':
            self.stats.add_backtrack()
        if action == 'success':
            self.stats.add_solution()
        self._update_stats()

    # ── Refresh Statistics Display ───────────────────────────────────────
    def _update_stats(self):
        self.lbl_attempts.config(text=f"{self.stats.attempts:,}")
        self.lbl_backtracks.config(text=f"{self.stats.backtracks:,}")
        self.lbl_solutions.config(text=f"{self.stats.solutions}")
        self.lbl_time.config(text=self.stats.runtime_str())

    def _status(self, msg):
        self.lbl_status.config(text=msg)

    # ── Benchmark ─────────────────────────────────────────────────
    def _run_benchmark(self):
        win = tk.Toplevel(self)
        win.title("Benchmark N-Queens")
        win.configure(bg=BG_MAIN)
        win.geometry("480x340")

        tk.Label(win, text="📊 Benchmark Results",
                 font=("Consolas", 14, "bold"),
                 bg=BG_MAIN, fg=ACCENT).pack(pady=12)

        frame = tk.Frame(win, bg=BG_CARD, padx=12, pady=12)
        frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=4)

        lbl_wait = tk.Label(frame, text="Running benchmark...",
                            font=FONT_LABEL, bg=BG_CARD, fg=FG_DIM)
        lbl_wait.pack(pady=20)

        def run():
            results = benchmark([4, 6, 8, 10, 12])
            win.after(0, lambda: _show(results))

        def _show(results):
            lbl_wait.destroy()
            # Table Header
            cols = ["N", "Solutions", "Attempts", "Backtracks", "Time"]
            widths = [4, 10, 12, 12, 10]
            header = tk.Frame(frame, bg=BG_CARD)
            header.pack(fill=tk.X)
            for i, (col, w) in enumerate(zip(cols, widths)):
                tk.Label(header, text=col, font=("Consolas", 10, "bold"),
                         bg=BG_CARD, fg=ACCENT, width=w,
                         anchor="e").pack(side=tk.LEFT)
            tk.Frame(frame, bg="#444466", height=1).pack(fill=tk.X, pady=4)
            # Result Rows
            for r in results:
                row = tk.Frame(frame, bg=BG_CARD)
                row.pack(fill=tk.X, pady=2)
                vals = [r['N'], r['solutions'], r['attempts'],
                        r['backtracks'], r['time']]
                for v, w in zip(vals, widths):
                    tk.Label(row, text=str(v), font=FONT_LABEL,
                             bg=BG_CARD, fg=FG_TEXT, width=w,
                             anchor="e").pack(side=tk.LEFT)

        threading.Thread(target=run, daemon=True).start()

