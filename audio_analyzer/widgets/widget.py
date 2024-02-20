from tkinter import Frame


class Widget:

    def __init__(self, master, app):
        self.master = master
        self.frame = Frame(master)
        self.app = app

    @property
    def pack(self):
        return self.frame.pack

    @property
    def pack_forget(self):
        return self.frame.pack_forget

    @property
    def grid(self):
        return self.frame.grid

    @property
    def grid_forget(self):
        return self.frame.grid_forget
