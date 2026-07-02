"""
main.py - Entry point của N-Queens Solver
Chạy: python main.py
"""
import tkinter as tk
from gui import App


def main():
    app = App()
    # Căn giữa màn hình
    app.update_idletasks()
    w, h = app.winfo_width(), app.winfo_height()
    sw = app.winfo_screenwidth()
    sh = app.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    app.geometry(f"+{x}+{y}")
    app.mainloop()


if __name__ == "__main__":
    main()

