import time
from tkinter import Frame

from audio_analyzer.utils.audio import lms_filter
from audio_analyzer.utils.threading import wait

from audio_analyzer.widgets.signal_visualisation import SignalVisualizer
from audio_analyzer.widgets.speech_recognition import SpeechRecognizer
from .screen import Screen


class MainScreen(Screen):

    def __init__(self, app):
        super().__init__(app, Frame(app.window, background='white', pady=20))

        self.audio_visualizer = SignalVisualizer(self.frame)
        self.audio_visualizer.grid(column=0, row=0)

        self.filtered_audio_visualizer = SignalVisualizer(self.frame)
        self.filtered_audio_visualizer.grid(column=1, row=0)

        self.speech_recognizer = SpeechRecognizer(self.frame)
        self.speech_recognizer.grid(column=0, row=1, columnspan=2)


    def pack(self):
        self.audio_visualizer.show('Recorded Audio', self.app.audio,
                                   self.app.play_audio)
        self.window.configure(background='white')
        super().pack()

        audio_lock = self.app.filter_audio(
            lambda audio: lms_filter(audio, step_size=0.001, filter_order=32))
        speech_recognition_lock = self.app.recognize_text()

        wait(audio_lock, speech_recognition_lock)

        self.filtered_audio_visualizer.show('Filtered Audio',
                                            self.app.filtered_audio,
                                            self.app.play_filtered_audio)
        self.speech_recognizer.show(self.app.recognized_text)
