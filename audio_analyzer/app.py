from tkinter import Tk
from tkinter.font import Font

from audio_analyzer.utils.audio import recognize_speech, record_audio, play_audio
from audio_analyzer.utils.threading import run_thread_with_lock
from audio_analyzer.utils import fonts
from navigator import Navigator
from screen import StartScreen, MainScreen
from PIL import Image, ImageTk
import threading


class App:

    def __init__(self) -> None:
        self.audio = None
        self.audio_recording_lock = threading.Lock()
        self.audio_playing_lock = threading.Lock()

        self.filtered_audio = None
        self.filtered_audio_playing_lock = threading.Lock()

        self.recognized_text = None
        self.recognize_text_lock = threading.Lock()

        self.window = Tk()
        self.window.title('VoiceVibe')
        ico = Image.open('style/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.window.wm_iconphoto(False, photo)
        self.center_window(self.window, 1450, 650)
        self.window.configure(background='black')


        self.fonts = fonts.Fonts()
        self.fonts.normal = Font(family="Times New Roman",
                                 size=15,
                                 weight='normal',
                                 slant='roman')

        self.fonts.bold = fonts.extend(self.fonts.normal, weight='bold')
        self.fonts.italic = fonts.extend(self.fonts.normal, slant='italic')

        self.fonts.title = fonts.extend(self.fonts.bold,
                                        size=self.fonts.bold['size'] + 3)

        self.window.option_add("*Font", self.fonts.normal)

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

    def filter_audio(self, filter, callback=None):

        def func():
            self.filtered_audio = filter(self.audio)
            if callback is not None: callback(self.filtered_audio)

        return run_thread_with_lock(self.filtered_audio_playing_lock, func)

    def play_filtered_audio(self):
        return run_thread_with_lock(self.filtered_audio_playing_lock,
                                    lambda: play_audio(self.filtered_audio))

    def recognize_text(self, callback=None):

        def func():
            self.recognized_text = recognize_speech(self.audio)
            if callback is not None: callback(self.recognized_text)

        return run_thread_with_lock(self.recognize_text_lock, func)
