from model import Model
from view import View
from controller import Controller
import tkinter as tk


class SoundApp:
    def __init__(self):
        self.root = tk.Tk()

        # creates instances of model, view, and controller
        self.model = Model()
        self.view = View(self.root, self.model)
        self.controller = Controller(self.model, self.view)

        # Start Tkinter main loop
        self.root.mainloop()


if __name__ == '__main__':
    app = SoundApp()  # runs main loop for program
