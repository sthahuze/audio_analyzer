
class Screen:
    def __init__(self, window, navigator, frame):
        self.window = window
        self.navigator = navigator
        self.frame = frame

    def pack(self):
        self.frame.pack()

    def pack_forget(self):
        self.frame.pack_forget()
