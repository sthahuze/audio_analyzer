import threading
import time
from tkinter import HORIZONTAL, Entry, Frame, Button, Label
from tkinter.ttk import Progressbar

from PIL import Image, ImageSequence, ImageTk

from .screen import Screen


class StartScreen(Screen):

    def __init__(self, app):
        super().__init__(app, Frame(app.window, background='black'))

        self.timer_label = Label(self.frame,
                                 bd=0,
                                 font=("Helvetica", 18),
                                 bg="black",
                                 fg="white")

        self.button = Button(self.frame,
                             text="Record my voice",
                             command=self.on_button_click,
                             bg="white",
                             fg="black",
                             font=("Open Sans", 20, "bold"),
                             width=23,
                             padx=25,
                             pady=15)
        self.button.grid(column=0, row=3, columnspan=2)

        self.duration_label = Label(self.frame,
                                    text='Duration (seconds)',
                                    bg='black',
                                    fg='white')
        self.duration_label.grid(column=0, row=4, pady=10)

        self.duration_entry = Entry(self.frame, width=4)
        self.duration_entry.grid(column=1, row=4, pady=10)
        self.duration_entry.insert(0, '5')

        self.progress = Progressbar(self.frame,
                                    orient=HORIZONTAL,
                                    length=100,
                                    mode='determinate')

    def pack(self):  # pyright: ignore
        self.show_gif()
        super().pack()

    def update_gif(self, frame_num, gif_frames, gif_label):
        frame = gif_frames[frame_num]
        gif_label.configure(image=frame)
        frame_num = (frame_num + 1) % len(gif_frames)
        self.window.after(
            100, lambda: self.update_gif(frame_num, gif_frames, gif_label))

    def show_gif(self):
        gif_image = Image.open("style/audio_wave.gif")
        gif_frames = [
            ImageTk.PhotoImage(img)
            for img in ImageSequence.Iterator(gif_image)
        ]

        gif_label = Label(self.frame, bd=0)
        gif_label.grid(column=0, row=0, columnspan=2)
        self.update_gif(0, gif_frames, gif_label)

    def on_button_click(self):
        duration = int(self.duration_entry.get())
        self.timer_label.grid(column=0, row=1, columnspan=2)
        self.progress.grid(column=0, row=2, columnspan=2)
        self.button.destroy()
        self.duration_label.destroy()
        self.duration_entry.destroy()

        audio_recording_lock = self.app.record_audio(duration)

        self.timer_label.config(text="Recording...")

        def target():
            self.bar(duration)

            while audio_recording_lock.locked():
                time.sleep(0.1)

            self.timer_label.config(text="Recording complete!")
            print("Recording complete!")
            self.navigator.open('main_screen')

        threading.Thread(target=target).start()

    def bar(self, duration):
        i = 0
        step = 100 / duration
        while i < 81:
            self.progress['value'] = int(i)
            self.frame.update_idletasks()
            time.sleep(1.)
            i += step
        self.progress['value'] = 100
