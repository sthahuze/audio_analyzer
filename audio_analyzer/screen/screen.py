
class Screen:
    def __init__(self, app, frame):
        self.app = app
        self.window = app.window
        self.navigator = app.navigator
        self.frame = frame

    def pack(self):
        self.frame.pack()

    def pack_forget(self):
        self.frame.pack_forget()
