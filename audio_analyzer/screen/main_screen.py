from tkinter import Frame, Label

from audio_analyzer.utils import audio

from audio_analyzer.widgets.signal_visualisation import SignalVisualizer
from audio_analyzer.widgets.speech_recognition import SpeechRecognizer
from audio_analyzer.widgets.emotion_recognition import EmotionRecognizer
from audio_analyzer.widgets.filter_menu import FilterMenu
from audio_analyzer.widgets.filter_settings import FilterSettings

from .screen import Screen


class Filter:

    def __init__(self, filter, **opts):
        self.filter = filter
        self.opts = opts


FILTERS = {
    'lms':
    Filter(audio.lms_filter, step_size=(float, 0.001), filter_order=(int, 32)),
    'reverbation':
    Filter(audio.reverb_filter,
           delay=(float, 0.1),
           decay=(float, 0.8),
           decay_coef=(float, 0.2),
           repetitions=(int, 2)),
    'band':
    Filter(audio.band_filter,
           low_freq=(int, 220),
           high_freq=(int, 5000),
           order=(int, 4)),
    'distortion':
    Filter(audio.distortion_filter, coef=(float, 5.), gain=(float, 5.))
}


class MainScreen(Screen):

    def __init__(self, app):
        super().__init__(app, Frame(app.window, pady=3, bg='white'))

        self.audio_visualizer = SignalVisualizer(self.frame, app)
        self.audio_visualizer.grid(column=0, row=0, rowspan=2)

        self.filtered_audio_visualizer = SignalVisualizer(self.frame, app)
        self.filtered_audio_visualizer.grid(column=1, row=0, rowspan=2)

        self.filter_menu = FilterMenu(self.frame, app, FILTERS)
        self.filter_menu.on_select(self.select_filter)
        self.filter_menu.grid(column=3, row=0, sticky='nw', pady=10)

        self.filtered_audio_settings = FilterSettings(self.frame, app, FILTERS)
        self.filtered_audio_settings.on_apply(self.apply_filter)
        self.filtered_audio_settings.grid(column=3,
                                          row=1,
                                          sticky='nw',
                                          pady=10)

        self.emotion_recognizer = EmotionRecognizer(self.frame, app)
        self.emotion_recognizer.grid(column=0, row=2, columnspan=3)

        self.speech_recognizer = SpeechRecognizer(self.frame, app)
        self.speech_recognizer.grid(column=0, row=3, columnspan=3)

    def pack(self):  # pyright: ignore
        self.audio_visualizer.show('Recorded Audio', self.app.audio,
                                   self.app.play_audio)
        self.filtered_audio_visualizer.show(title=f'Filtered Audio: original',
                                            audio=self.app.audio,
                                            play_audio=self.app.play_audio)
        self.window.configure(bg='white')
        super().pack()

        self.app.recognize_emotion(callback=lambda recognized_emotion: self.
                                   emotion_recognizer.show(recognized_emotion))

        self.app.recognize_text(callback=lambda recognized_text: self.
                                speech_recognizer.show(recognized_text))

    def select_filter(self, filter_type):
        self.filtered_audio_settings.select_filter(filter_type)

    def apply_filter(self, filter_type, filter):

        def callback(filtered_audio):
            self.filtered_audio_visualizer.show(
                title=f'Filtered Audio: {filter_type}',
                audio=filtered_audio,
                play_audio=self.app.play_filtered_audio)

        self.app.filter_audio(filter, callback)
