from tkinter import Frame, Label
from PIL import ImageTk, Image


class SpeechRecognizer:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(master)

        self.recognition_frame =  Frame(self.frame)
        self.recognition_frame.grid(column=0, row=1, columnspan=2)

        self.photo = ImageTk.PhotoImage(Image.open("style/happy.jpg").resize((100, 100)))
        Label(self.recognition_frame, image=self.photo).grid(column=0, row=0)

        self.label = Label(self.recognition_frame, font=("Times New Roman", 20), bg="white")
        self.label.grid(column=1, row=0)


    def show(self, text):
        self.label.config(text=text)

    @property
    def pack(self):
        return self.frame.pack

    @property
    def pack_forget(self):
        return self.frame.pack_forget

    @property
    def grid(self):
        return self.frame.grid

    @property
    def grid_forget(self):
        return self.frame.grid_forget
