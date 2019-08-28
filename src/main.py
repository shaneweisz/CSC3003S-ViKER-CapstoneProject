from gui import GUI
from controller import Controller
import tkinter as tk


def main():
    gui = GUI(tk.Tk())
    c = Controller(gui)
    gui.window.mainloop()


if __name__ == '__main__':
    main()
