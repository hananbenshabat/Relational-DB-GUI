import tkinter as tk


# A type of Label that automatically adjusts the wrap to the size
class WrappingLabel(tk.Label):
    def __init__(self, master=None):
        tk.Label.__init__(self, master)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))
