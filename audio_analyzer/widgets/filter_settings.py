from tkinter import Entry, Label, Frame, Button
from audio_analyzer.utils import Notifier
from audio_analyzer.widgets.widget import Widget
from audio_analyzer.utils import audio


class Filter:

    def __init__(self, filter, **opts):
        self.filter = filter
        self.opts = opts


class FilterSettings(Widget):
    FILTERS = {
        'lms':
        Filter(audio.lms_filter,
               step_size=(float, 0.001),
               filter_order=(int, 32))
    }

    def __init__(self, master):
        super().__init__(master)
        self.title = Label(self.frame)
        self.title.grid(row=0, column=0)

        self.settings_frame = Frame(self.frame)
        self.settings_frame.grid(row=1, column=0)

        self.apply_button = Button(self.frame,
                                   text='Apply',
                                   width=30,
                                   command=self.apply)
        self.apply_button.grid(row=2, column=0)

        self.apply_notifier = Notifier()
        self.entries = {}
        self.select_filter('lms')

    def select_filter(self, filter_type):
        self.filter_type = filter_type
        f = self.FILTERS[filter_type]
        self.filter = f.filter
        default_opts = f.opts

        self.title.configure(text=f'Filter Settings: {self.filter_type}')

        self.clear_settings()
        self.entries.clear()

        for i, (opt, (_, value)) in enumerate(default_opts.items(), start=1):
            label = Label(self.settings_frame, text=' '.join(opt.split('_')))
            label.grid(row=i, column=0, sticky='w')

            entry = Entry(self.settings_frame)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1)

            self.entries[opt] = entry

    def clear_settings(self):
        for _, widget in self.settings_frame.children.items():
            widget.grid_forget()

    def on_apply(self, handler):
        self.apply_notifier.register(handler)

    def apply(self):
        filter_opts = {}
        for key, entry in self.entries.items():
            deserialize = self.FILTERS[self.filter_type].opts[key][0]
            filter_opts[key] = deserialize(entry.get())

        self.apply_notifier.notify(
            self.filter_type, lambda audio: self.filter(audio, **filter_opts))
