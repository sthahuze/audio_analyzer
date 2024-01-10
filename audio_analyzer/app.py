from tkinter import Tk

from audio_analyzer.utils.audio import record_audio, play_audio
from .navigator import Navigator
from .screen import StartScreen, MainScreen
import threading


class App:

    def __init__(self) -> None:
        self.audio = None
        self.audio_recording_lock = threading.Lock()
        self.audio_playing_lock = threading.Lock()

        self.window = Tk()
        self.window.title('Audio analyser')
        self.center_window(self.window, 1200, 650)
        self.window.configure(background='black')

        self.navigator = Navigator(self.window)
        self.navigator.set_screens(start_screen=StartScreen(self),
                                   main_screen=MainScreen(self))
        self.navigator.open('start_screen')

    def run(self):
        self.window.mainloop()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 50

        window.geometry(f"{width}x{height}+{x}+{y}")

    def record_audio(self):
        if self.audio_recording_lock.locked(): return

        def target():
            self.audio_recording_lock.acquire()
            self.audio = record_audio()
            self.audio_recording_lock.release()

        threading.Thread(target=target).start()

        return self.audio_recording_lock

    def play_audio(self):
        if self.audio_playing_lock.locked(): return

        def target():
            self.audio_playing_lock.acquire()
            play_audio(self.audio)
            self.audio_playing_lock.release()

        threading.Thread(target=target).start()

        return self.audio_playing_lock
