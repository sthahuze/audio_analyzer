from tkinter import Button, Label
from audio_analyzer.widgets.widget import Widget
from audio_analyzer.utils import audio, Notifier, deref


class FilterMenu(Widget):
    def __init__(self, master, app, filters):
        super().__init__(master, app)
        self.filters = filters
        self.select_notifier = Notifier()
        self.title = Label(self.frame, text='Filter Menu')
        self.title.grid(row=0, column=0)
        self.buttons = []

        for i, filter_type in enumerate(self.filters, start=1):
            button = Button(self.frame,
                            text=filter_type,
                            width=30,
                            command=deref(
                                filter_type,
                                lambda filter_type: self.select(filter_type)))
            button.grid(row=i, column=0)
            self.buttons.append(button)

    def on_select(self, handler):
        self.select_notifier.register(handler)

    def select(self, filter_type):
        self.select_notifier.notify(filter_type)
