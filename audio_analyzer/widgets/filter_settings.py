from tkinter import Entry, Label, Frame, Button
from audio_analyzer.utils import Notifier
from audio_analyzer.widgets.widget import Widget


class FilterSettings(Widget):

    def __init__(self, master, app, filters):
        super().__init__(master, app)
        self.filters = filters

        self.title = Label(self.frame, bg='white')
        self.title.grid(row=0, column=0, columnspan=2)

        self.apply_button = Button(self.frame,
                                   text='Apply',
                                   width=20,
                                   bg='white',
                                   command=self.apply)

        self.apply_notifier = Notifier()
        self.entries = {}
        self.settings_widgets = []
        self.select_filter('lms')

    def select_filter(self, filter_type):
        self.filter_type = filter_type
        f = self.filters[filter_type]
        self.filter = f.filter
        default_opts = f.opts

        self.title.configure(text=f'Filter Settings: {self.filter_type}')

        self.clear_settings()
        self.entries.clear()

        i = 1
        for i, (opt, (_, value)) in enumerate(default_opts.items(), start=1):
            label = Label(self.frame, text=' '.join(opt.split('_')), bg='white')
            label.grid(row=i, column=0, sticky='w')

            entry = Entry(self.frame, width=10)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, sticky='e')

            self.settings_widgets.append(label)
            self.settings_widgets.append(entry)

            self.entries[opt] = entry

        self.apply_button.grid(row=i + 1, column=0, columnspan=2)

    def clear_settings(self):
        for widget in self.settings_widgets:
            widget.grid_forget()
        self.settings_widgets.clear()

    def on_apply(self, handler):
        self.apply_notifier.register(handler)

    def apply(self):
        filter_opts = {}
        for key, entry in self.entries.items():
            deserialize = self.filters[self.filter_type].opts[key][0]
            filter_opts[key] = deserialize(entry.get())

        self.apply_notifier.notify(
            self.filter_type, lambda audio: self.filter(audio, **filter_opts))
