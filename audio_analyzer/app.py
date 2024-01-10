from tkinter import Tk

from audio_analyzer.utils.audio import record_audio, play_audio
from audio_analyzer.utils.threading import run_thread_with_lock
from .navigator import Navigator
from .screen import StartScreen, MainScreen
import threading


class App:

    def __init__(self) -> None:
        self.audio = None
        self.audio_recording_lock = threading.Lock()
        self.audio_playing_lock = threading.Lock()

        self.filtered_audio = None
        self.filtered_audio_playing_lock = threading.Lock()

        self.window = Tk()
        self.window.title('Audio analyzer')
        self.center_window(self.window, 1200, 650)
        self.window.configure(background='black')

        self.navigator = Navigator(self.window)
        self.navigator.set_screens(start_screen=StartScreen(self),
                                   main_screen=MainScreen(self))

    def run(self):
        print('Starting the application')
        self.navigator.open('start_screen')
        self.window.mainloop()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 50

        window.geometry(f"{width}x{height}+{x}+{y}")

    def record_audio(self):

        def func():
            self.audio = record_audio()

        return run_thread_with_lock(self.audio_playing_lock, func)

    def play_audio(self):
        return run_thread_with_lock(self.audio_playing_lock,
                                    lambda: play_audio(self.audio))

    def filter_audio(self, filter):

        def func():
            self.filtered_audio = filter(self.audio)

        return run_thread_with_lock(self.filtered_audio_playing_lock, func)

    def play_filtered_audio(self):
        return run_thread_with_lock(self.filtered_audio_playing_lock,
                                    lambda: play_audio(self.filtered_audio))
