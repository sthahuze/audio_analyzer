
class Screen:
    def __init__(self, app, frame):
        self.app = app
        self.window = app.window
        self.navigator = app.navigator
        self.frame = frame

    @property
    def pack(self): return self.frame.pack

    @property
    def pack_forget(self): return self.frame.pack_forget
