class Navigator:
    def __init__(self, window):
        self.window = window
        self.screens = {}
        self.current_screen = None

    def set_screens(self, **kwargs):
        self.screens = kwargs

    def open(self, screen_name):
        if self.current_screen is not None: self.current_screen.pack_forget()
        self.current_screen = self.screens[screen_name]
        self.current_screen.pack()
