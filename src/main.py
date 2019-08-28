from view import GUI
from controller import Controller
import tkinter as tk


def main():
    """Runs the application."""
    gui = GUI(tk.Tk())
    c = Controller(gui)
    gui.window.mainloop()


if __name__ == '__main__':
    main()
