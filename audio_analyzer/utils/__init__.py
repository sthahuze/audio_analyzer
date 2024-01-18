from . import audio, threading

class Notifier:
    def __init__(self):
        self.handlers = []

    def register(self, handler):
        self.handlers.append(handler)

    def notify(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)

def deref(value, func):
    return lambda: func(value)
