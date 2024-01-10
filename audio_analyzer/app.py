from tkinter import Tk
from .navigator import Navigator
from .screen import StartScreen, MainScreen

class App:
    def __init__(self) -> None:
        self.master = Tk()
        self.navigator = Navigator(self.master)
        self.navigator.set_screens(
            start_screen = StartScreen(self.master, self.navigator),
            main_screen = MainScreen(self.master, self.navigator)
        )
        self.navigator.open('start_screen')
        self.master.title('Audio analyser')
        self.center_window(self.master, 1200, 650)
        self.master.configure(background='black')

    def run(self):
        self.master.mainloop()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 50

        window.geometry(f"{width}x{height}+{x}+{y}")
