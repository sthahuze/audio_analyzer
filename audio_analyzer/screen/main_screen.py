
from tkinter import Frame

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .screen import Screen
from visualisation import fourier_analysis, show_spectrogram, unwrapped_phase_spectrum, wave_show


class MainScreen(Screen):
    def __init__(self, window, navigator):
        super().__init__(window, navigator, Frame(window, background='white'))

        self.canvas_frame = Frame(self.frame, background='white')
        self.changes_frame = Frame(self.frame, background='white')

    def pack(self):
        super().pack()
        self.create_canvas("wave_show")
        self.window.configure(background='white')

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
