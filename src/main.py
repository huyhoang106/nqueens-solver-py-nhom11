"""
main.py - Entry point for the N-Queens Solver application.

Run:
    python main.py
"""

import tkinter as tk
from gui import App


def main():
    """Launch the N-Queens Solver graphical application."""

    app = App()

    # Center the application window on the screen
    app.update_idletasks()
    w, h = app.winfo_width(), app.winfo_height()
    sw = app.winfo_screenwidth()
    sh = app.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    app.geometry(f"+{x}+{y}")

    # Start the Tkinter event loop
    app.mainloop()


if __name__ == "__main__":
    main()
