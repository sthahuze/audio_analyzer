from tkinter import Frame, Label
from PIL import ImageTk, Image

from audio_analyzer.widgets.widget import Widget


class SpeechRecognizer(Widget):

    def __init__(self, master, app):
        super().__init__(master, app)

        self.recognition_frame = Frame(self.frame)
        self.recognition_frame.grid(column=0, row=1, columnspan=2)

        self.label = Label(self.recognition_frame)
        self.label.grid(column=0, row=0)

        self.label = Label(self.recognition_frame)
        self.label.grid(column=1, row=0)

    def show(self, text):
        self.label.config(text=text)
