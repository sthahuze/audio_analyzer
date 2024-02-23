from audio_analyzer.widgets.widget import Widget
from tkinter import Frame, Label


class EmotionRecognizer(Widget):

    def __init__(self, master, app):
        super().__init__(master, app)

        self.recognition_frame = Frame(self.frame, bg='white')
        self.recognition_frame.grid(column=0, row=0, columnspan=2)

        self.label = Label(self.recognition_frame,
                           text='Emotion Recognition: recognizing...',
                           font=('Times New Roman', 18),
                           bg='white')
        self.label.grid(column=0, row=0)

    def show(self, emotions):
        text = ', '.join(emotions)
        self.label.config(text=f'Emotion Recognition: {text}')
