
import threading
import time
from tkinter import HORIZONTAL, Frame, Button, Label
from tkinter.ttk import Progressbar

from PIL import Image, ImageSequence, ImageTk

from .screen import Screen
from ..write_sound import record_audio


class StartScreen(Screen):
    def __init__(self, window, navigator):
        super().__init__(window, navigator, Frame(window, background = 'black'))

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
                             font=("Times New Roman", 20, "bold"),
                             padx=30,
                             pady=15)

        self.progress = Progressbar(self.frame,
                                    orient=HORIZONTAL,
                                    length=100,
                                    mode='determinate')

        self.button.grid(column=0, row=3)

    def pack(self):
        super().pack()
        self.show_gif()


    def update_gif(self, frame_num, gif_frames, gif_label):
        frame = gif_frames[frame_num]
        gif_label.configure(image=frame)
        frame_num = (frame_num + 1) % len(gif_frames)
        self.window.after(
            100, lambda: self.update_gif(frame_num, gif_frames, gif_label))

    def show_gif(self):
        gif_image = Image.open("assets/audio_wave.gif")
        gif_frames = [
            ImageTk.PhotoImage(img)
            for img in ImageSequence.Iterator(gif_image)
        ]

        gif_label = Label(self.frame, bd=0)
        gif_label.grid(column=0, row=0)
        self.update_gif(0, gif_frames, gif_label)

    def record_audio_with_timer(self):
        record_audio()
        print("Recording complete!")
        self.navigator.open('main_screen')

    def on_button_click(self):
        self.timer_label.grid(column=0, row=1)
        self.progress.grid(column=0, row=2)
        self.button.destroy()
        # Початок запису голосу в окремому потоці
        thread = threading.Thread(target=self.record_audio_with_timer)
        thread.start()

        thread2 = threading.Thread(target=self.bar)
        thread2.start()

        # Оновлення таймера
        self.timer_label.config(
            text="Recording..."
        )  # Початок запису, тут ви можете відобразити таймер
        self.window.after(
            5000, lambda: self.timer_label.config(text="Recording complete!"))

    def bar(self):
        for i in range(0, 81, 20):
            self.progress['value'] = i
            self.frame.update_idletasks()
            time.sleep(1.)
        self.progress['value'] = 100
