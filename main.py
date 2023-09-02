import _tkinter

from algo import Algo
from interface import Interface

import customtkinter as ctk
from tkinter import messagebox
from tkinter import simpledialog


class Minesweeper:
    def __init__(self):
        self.size = [10, 10]
        self.mine_number = 15

        self.ask_level()
        self.init_algo()
        self.interface = Interface(self)
        self.interface.mainloop()

    def init_algo(self):
        self.algo = Algo(tuple(self.size), self.mine_number)
        self.algo.print()

    def ask_level(self):
        self.window = ctk.CTk()
        self.window.title("Choose a difficulty")
        self.window.geometry(f"{275}x{200}")

        button_easy = ctk.CTkButton(master=self.window, text="Easy", command=lambda: self.handle_difficulty_chosen(0))
        button_easy.pack(pady=10)

        button_intermediate = ctk.CTkButton(master=self.window, text="Intermediate", command=lambda: self.handle_difficulty_chosen(1))
        button_intermediate.pack(pady=10)

        button_hard = ctk.CTkButton(master=self.window, text="Hard", command=lambda: self.handle_difficulty_chosen(2))
        button_hard.pack(pady=10)

        button_custom = ctk.CTkButton(master=self.window, text="Custom", command=lambda: self.handle_difficulty_chosen(3))
        button_custom.pack(pady=(10, 0))

        self.window.mainloop()

    def retry(self, difficulty):
        self.handle_difficulty_chosen(difficulty)
        self.init_algo()
        self.interface.destroy()
        self.interface = Interface(self)
        self.interface.mainloop()

    def handle_difficulty_chosen(self, difficulty):
        try:
            self.window.destroy()
        except _tkinter.TclError:
            pass

        match difficulty:
            case 0:
                # easy
                print("easy")
                self.size = (10, 10)
                self.mine_number = 10
            case 1:
                # intermediate
                print("intermediate")
                self.size = (16, 16)
                self.mine_number = 40
            case 2:
                # hard
                print("hard")
                self.size = (30, 16)
                self.mine_number = 99
            case 3:
                # custom
                print("custom")
                self.custom()

    def custom(self):
        """Ask the user what values he wants"""
        # ask the size of the grid
        self.size = [10, 10]
        size = simpledialog.askinteger(title="Grid Size", prompt="X → Left to right")
        self.size[0] = self.test_custom_size(size)

        size = simpledialog.askinteger(title="Grid Size", prompt="Y → Top to bottom")
        self.size[1] = self.test_custom_size(size)

        # ask the number of mine
        mine_number = simpledialog.askinteger(title="Mine Number", prompt="How many mine do you want ?")
        self.mine_number = self.test_custom_mine_number(mine_number)

    @staticmethod
    def test_custom_size(number):
        try:
            assert type(number) == int
            assert number > 1
        except AssertionError:
            messagebox.showwarning(title="Invalid number", message="Your number was incorrect.\nValue put to 10")
            return 10
        return number

    def test_custom_mine_number(self, mine_number):
        try:
            assert type(mine_number) == int
            assert mine_number > 0
            assert mine_number < (self.size[0] * self.size[1])
        except AssertionError:
            messagebox.showwarning(title="Invalid number", message="Your number was incorrect.\nValue put to 15")
            return 15
        return mine_number


if __name__ == '__main__':
    app = Minesweeper()
