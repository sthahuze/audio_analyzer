from tkinter import Button, Frame, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.signal import spectrogram
from matplotlib.figure import Figure

from audio_analyzer.widgets.widget import Widget


def wave_show(audio, state="min"):
    audio_data, sample_rate = audio
    time = np.arange(0, len(audio_data)) / sample_rate
    if state == "min":
        fig = Figure(figsize=(2, 1.33), dpi=100)
        ax = fig.add_subplot()
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot()
        ax.set_title('Waveform of Audio Signal (Volume)')
        ax.set_xlabel('Time (s)')
    ax.plot(time, audio_data)

    return fig


def fourier_analysis(audio, state="min"):
    audio_data, sample_rate = audio
    # Perform Fourier transform on the audio signal
    fourier_transform = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(fourier_transform), 1 / sample_rate)
    amplitudes = np.abs(fourier_transform)

    if state == "min":
        fig = Figure(figsize=(2, 1.33), dpi=100)
        ax = fig.add_subplot()
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot()
        ax.set_title('Fourier Analysis')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude')

    ax.plot(frequencies, amplitudes)

    return fig


def show_spectrogram(audio, state="min"):
    # Compute and display the spectrogram of the audio signal
    audio_data, sample_rate = audio
    f, t, Sxx = spectrogram(audio_data, sample_rate)

    Sxx[Sxx == 0] = np.finfo(float).eps

    if state == "min":
        fig = Figure(figsize=(2, 1.33), dpi=100)
        ax = fig.add_subplot()
        ax.pcolormesh(t, f, 10 * np.log10(Sxx))
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot()
        ax.pcolormesh(t, f, 10 * np.log10(Sxx))
        ax.set_ylabel('Frequency (Hz)')
        ax.set_xlabel('Time (s)')
        ax.set_title('Spectrogram')

    return fig


def unwrapped_phase_spectrum(audio, state="min"):
    # Analyze the phase information of the Fourier transform
    audio_data, sample_rate = audio
    fourier_transform = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(fourier_transform), 1 / sample_rate)
    phases = np.angle(fourier_transform)
    phases_unwrapped = np.unwrap(phases)

    if state == "min":
        fig = Figure(figsize=(2, 1.33), dpi=100)
        ax = fig.add_subplot()
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot()
        ax.set_title('Unwrapped Phase Spectrum')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Phase')

    ax.plot(frequencies, phases_unwrapped)

    return fig


class SignalVisualizer(Widget):

    def __init__(self, master, app):
        super().__init__(master, app)

        self.audio = None

        self.title = Label(self.frame, font=app.fonts.bold, bg='white')
        self.title.grid(column=0, row=0, sticky='w', padx=10, pady=4)

        self.play_button = Button(self.frame,
                                  text='Play',
                                  width=5,
                                  bg='white',
                                  font=app.fonts.bold)
        self.play_button.grid(column=1, row=0, sticky='e', padx=10, pady=4)

        self.canvas = Frame(self.frame, bg='white')
        self.canvas.grid(column=0, row=1, columnspan=2, padx=5)

    def show(self, title, audio, play_audio):
        self.title.config(text=title)
        self.audio = audio
        self.play_button.config(command=play_audio)
        self.create_canvas('wave_show')

    def create_canvas(self, main_element):

        if main_element == "wave_show":
            fig1 = wave_show(self.audio, state="max")
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=0, columnspan=3)

            fig2 = show_spectrogram(self.audio)
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=0, row=1)

            fig3 = unwrapped_phase_spectrum(self.audio)
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=1, row=1)

            fig4 = fourier_analysis(self.audio)
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=2, row=1)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

        elif main_element == "show_spectrogram":

            fig1 = wave_show(self.audio)
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=1)

            fig2 = show_spectrogram(self.audio, state="max")
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=0, row=0, columnspan=3)

            fig3 = unwrapped_phase_spectrum(self.audio)
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=1, row=1)

            fig4 = fourier_analysis(self.audio)
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=2, row=1)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

        elif main_element == "unwrapped_phase_spectrum":

            fig1 = wave_show(self.audio)
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=1)

            fig2 = show_spectrogram(self.audio)
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=1, row=1)

            fig3 = unwrapped_phase_spectrum(self.audio, state="max")
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=0, row=0, columnspan=3)

            fig4 = fourier_analysis(self.audio)
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=2, row=1)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

        elif main_element == "fourier_analysis":

            fig1 = wave_show(self.audio)
            canvas1 = FigureCanvasTkAgg(fig1, master=self.canvas)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.grid(column=0, row=1)

            fig2 = show_spectrogram(self.audio)
            canvas2 = FigureCanvasTkAgg(fig2, master=self.canvas)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.grid(column=1, row=1)

            fig3 = unwrapped_phase_spectrum(self.audio)
            canvas3 = FigureCanvasTkAgg(fig3, master=self.canvas)
            canvas_widget3 = canvas3.get_tk_widget()
            canvas_widget3.grid(column=2, row=1)

            fig4 = fourier_analysis(self.audio, state="max")
            canvas4 = FigureCanvasTkAgg(fig4, master=self.canvas)
            canvas_widget4 = canvas4.get_tk_widget()
            canvas_widget4.grid(column=0, row=0, columnspan=3)

            canvas_widget1.bind('<Button-1>', self.on_canvas1_click)
            canvas_widget2.bind('<Button-1>', self.on_canvas2_click)
            canvas_widget3.bind('<Button-1>', self.on_canvas3_click)
            canvas_widget4.bind('<Button-1>', self.on_canvas4_click)

    def on_canvas1_click(self, event):
        self.create_canvas("wave_show")

    def on_canvas2_click(self, event):
        self.create_canvas("show_spectrogram")

    def on_canvas3_click(self, event):
        self.create_canvas("unwrapped_phase_spectrum")

    def on_canvas4_click(self, event):
        self.create_canvas("fourier_analysis")
