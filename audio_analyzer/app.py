from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from .write_sound import record_audio
import threading
from tkinter.ttk import Progressbar
import time
from visualisation import wave_show, show_spectrogram, unwrapped_phase_spectrum, fourier_analysis
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:

    def __init__(self) -> None:
        self.master = Tk()
        self.starter_frame = Frame(self.master, background='black')
        self.main_frame = Frame(self.master, background='white')
        self.starter_frame.pack()
        self.master.title('Audio analyser')
        self.center_window(self.master, 1200, 650)
        self.master.configure(background='black')

        self.timer_label = Label(self.starter_frame,
                                 bd=0,
                                 font=("Helvetica", 18),
                                 bg="black",
                                 fg="white")
        self.button = Button(self.starter_frame,
                             text="Record my voice",
                             command=self.on_button_click,
                             bg="white",
                             fg="black",
                             font=("Times New Roman", 20, "bold"),
                             padx=30,
                             pady=15)
        self.progress = Progressbar(self.starter_frame,
                                    orient=HORIZONTAL,
                                    length=100,
                                    mode='determinate')

        self.button.grid(column=0, row=3)
        self.show_gif()
        self.canvas_frame = Frame(self.main_frame, background='white')

        self.changes_frame = Frame(self.main_frame, background='white')

    def run(self):
        self.master.mainloop()

    def update_gif(self, frame_num, gif_frames, gif_label):
        frame = gif_frames[frame_num]
        gif_label.configure(image=frame)
        frame_num = (frame_num + 1) % len(gif_frames)
        self.master.after(
            100, lambda: self.update_gif(frame_num, gif_frames, gif_label))

    def show_gif(self):
        gif_image = Image.open("assets/audio_wave.gif")
        gif_frames = [
            ImageTk.PhotoImage(img)
            for img in ImageSequence.Iterator(gif_image)
        ]

        gif_label = Label(self.starter_frame, bd=0)
        gif_label.grid(column=0, row=0)
        self.update_gif(0, gif_frames, gif_label)

    def record_audio_with_timer(self):
        record_audio()
        print("Recording complete!")
        time.sleep(0.1)
        self.starter_frame.pack_forget()
        self.main_frame.pack()
        self.create_canvas("wave_show")
        self.master.configure(background='white')

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
        self.master.after(
            5000, lambda: self.timer_label.config(text="Recording complete!"))

    def bar(self):
        self.progress['value'] = 20
        self.starter_frame.update_idletasks()
        time.sleep(1)

        self.progress['value'] = 40
        self.starter_frame.update_idletasks()
        time.sleep(1)

        self.progress['value'] = 50
        self.starter_frame.update_idletasks()
        time.sleep(1)

        self.progress['value'] = 60
        self.starter_frame.update_idletasks()
        time.sleep(1)

        self.progress['value'] = 80
        self.starter_frame.update_idletasks()
        time.sleep(1)
        self.progress['value'] = 100

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 50

        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_canvas(self, main_element):
        self.canvas_frame.grid_forget()

        if main_element == "wave_show":
            fig1 = wave_show(state="max")
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas_frame)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=0, columnspan=3)

            fig2 = show_spectrogram()
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas_frame)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=0, row=1)

            fig3 = unwrapped_phase_spectrum()
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas_frame)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=1, row=1)

            fig4 = fourier_analysis()
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas_frame)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=2, row=1)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

        elif main_element == "show_spectrogram":

            fig1 = wave_show()
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas_frame)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=1)

            fig2 = show_spectrogram(state="max")
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas_frame)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=0, row=0, columnspan=3)

            fig3 = unwrapped_phase_spectrum()
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas_frame)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=1, row=1)

            fig4 = fourier_analysis()
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas_frame)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=2, row=1)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

        elif main_element == "unwrapped_phase_spectrum":

            fig1 = wave_show()
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas_frame)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=1)

            fig2 = show_spectrogram()
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas_frame)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=1, row=1)

            fig3 = unwrapped_phase_spectrum(state="max")
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas_frame)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=0, row=0, columnspan=3)

            fig4 = fourier_analysis()
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas_frame)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=2, row=1)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

        elif main_element == "fourier_analysis":

            fig1 = wave_show()
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas_frame)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=1)

            fig2 = show_spectrogram()
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas_frame)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=1, row=1)

            fig3 = unwrapped_phase_spectrum()
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas_frame)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=2, row=1)

            fig4 = fourier_analysis(state="max")
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas_frame)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=0, row=0, columnspan=3)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

        self.canvas_frame.grid(column=0, row=0)

    def on_canvas1_click(self, event):
        self.create_canvas("wave_show")

    def on_canvas2_click(self, event):
        self.create_canvas("show_spectrogram")

    def on_canvas3_click(self, event):
        self.create_canvas("unwrapped_phase_spectrum")

    def on_canvas4_click(self, event):
        self.create_canvas("fourier_analysis")
