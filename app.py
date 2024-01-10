from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from write_sound import record_audio
import threading
from tkinter.ttk import Progressbar
import time
from visualisation import wave_show, show_spectrogram, unwrapped_phase_spectrum, fourier_analysis
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from recognition import recognize_speech_from_audio
from reverbation import apply_hall, play_audio


photo = None


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2 - 50

    window.geometry(f"{width}x{height}+{x}+{y}")


def update_gif(frame_num, gif_frames, gif_label):
    frame = gif_frames[frame_num]
    gif_label.configure(image=frame)
    frame_num = (frame_num + 1) % len(gif_frames)
    master.after(100, lambda: update_gif(frame_num, gif_frames, gif_label))


def show_gif():
    gif_image = Image.open("style/audio_wave.gif")
    gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif_image)]

    gif_label = Label(starter_frame, bd=0)
    gif_label.grid(column=0, row=0)
    update_gif(0, gif_frames, gif_label)


def show_changes(fig):
    canvas = FigureCanvasTkAgg(fig, master=changes_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(column=0, row=0, columnspan=2)


def reverb():
    reverb_signal, fig = apply_hall()
    show_changes(fig)
    thread = threading.Thread(target=lambda: play_audio(reverb_signal))
    thread.start()


def prepare_main_frame():
    global photo
    time.sleep(0.01)
    timer_label.destroy()
    progress.destroy()
    Label(starter_frame, text="Preparing...", font=("Times New Roman", 30), bg="black", fg="white").grid(column=0,
                                                                                                         row=1)

    recognition_frame = Frame(main_frame, background='white')

    photo = ImageTk.PhotoImage(Image.open("style/happy.jpg").resize((100, 100)))
    Label(recognition_frame, image=photo).grid(column=0, row=0)

    recognised_text = recognize_speech_from_audio("temp.wav")
    l = Label(recognition_frame, text=recognised_text, font=("Times New Roman", 20), bg="white")
    l.grid(column=1, row=0)

    recognition_frame.grid(column=0, row=1, columnspan=2)

    reverb_signal, fig = apply_hall()
    show_changes(fig)

    reverb_Button = Button(changes_frame, text="Reverb", command=reverb, bg="white", fg="black", font=("Times New Roman", 16, "bold"), padx=5, pady=5, width=20, height=1)
    reverb_Button.grid(column=0, row=1)

    noise_cancel_Button = Button(changes_frame, text="Cancel noise", command=reverb, bg="white", fg="black", font=("Times New Roman", 16, "bold"), padx=5, pady=5, width=20, height=1)
    noise_cancel_Button.grid(column=1, row=1)

    changes_frame.grid(column=1, row=0)
    create_canvas("wave_show")

    starter_frame.pack_forget()
    master.configure(background='white')
    main_frame.pack()


def record_audio_with_timer():
    record_audio()
    print("Recording complete!")
    time.sleep(0.1)
    prepare_main_frame()


def on_button_click():
    timer_label.grid(column=0, row=1)
    progress.grid(column=0, row=2)
    button.destroy()
    # Початок запису голосу в окремому потоці
    thread = threading.Thread(target=record_audio_with_timer)
    thread.start()

    thread2 = threading.Thread(target=bar)
    thread2.start()

    timer_label.config(text="Recording...")
    master.after(5000, lambda: timer_label.config(text="Recording complete!"))


def bar():
    progress['value'] = 20
    starter_frame.update_idletasks()
    time.sleep(1)

    progress['value'] = 40
    starter_frame.update_idletasks()
    time.sleep(1)

    progress['value'] = 50
    starter_frame.update_idletasks()
    time.sleep(1)

    progress['value'] = 60
    starter_frame.update_idletasks()
    time.sleep(1)

    progress['value'] = 80
    starter_frame.update_idletasks()
    time.sleep(1)
    progress['value'] = 100


def create_canvas(main_element):
    canvas_frame.grid_forget()

    if main_element == "wave_show":
        fig1 = wave_show(state="max")
        canvas1 = FigureCanvasTkAgg(fig1, master=canvas_frame)
        canvas_widget1 = canvas1.get_tk_widget()
        canvas_widget1.grid(column=0, row=0, columnspan=3)

        fig2 = show_spectrogram()
        canvas2 = FigureCanvasTkAgg(fig2, master=canvas_frame)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.grid(column=0, row=1)

        fig3 = unwrapped_phase_spectrum()
        canvas3 = FigureCanvasTkAgg(fig3, master=canvas_frame)
        canvas_widget3 = canvas3.get_tk_widget()
        canvas_widget3.grid(column=1, row=1)

        fig4 = fourier_analysis()
        canvas4 = FigureCanvasTkAgg(fig4, master=canvas_frame)
        canvas_widget4 = canvas4.get_tk_widget()
        canvas_widget4.grid(column=2, row=1)

        canvas_widget1.bind('<Button-1>', on_canvas1_click)
        canvas_widget2.bind('<Button-1>', on_canvas2_click)
        canvas_widget3.bind('<Button-1>', on_canvas3_click)
        canvas_widget4.bind('<Button-1>', on_canvas4_click)

    elif main_element == "show_spectrogram":

        fig1 = wave_show()
        canvas1 = FigureCanvasTkAgg(fig1, master=canvas_frame)
        canvas_widget1 = canvas1.get_tk_widget()
        canvas_widget1.grid(column=0, row=1)

        fig2 = show_spectrogram(state="max")
        canvas2 = FigureCanvasTkAgg(fig2, master=canvas_frame)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.grid(column=0, row=0, columnspan=3)

        fig3 = unwrapped_phase_spectrum()
        canvas3 = FigureCanvasTkAgg(fig3, master=canvas_frame)
        canvas_widget3 = canvas3.get_tk_widget()
        canvas_widget3.grid(column=1, row=1)

        fig4 = fourier_analysis()
        canvas4 = FigureCanvasTkAgg(fig4, master=canvas_frame)
        canvas_widget4 = canvas4.get_tk_widget()
        canvas_widget4.grid(column=2, row=1)

        canvas_widget1.bind('<Button-1>', on_canvas1_click)
        canvas_widget2.bind('<Button-1>', on_canvas2_click)
        canvas_widget3.bind('<Button-1>', on_canvas3_click)
        canvas_widget4.bind('<Button-1>', on_canvas4_click)

    elif main_element == "unwrapped_phase_spectrum":

        fig1 = wave_show()
        canvas1 = FigureCanvasTkAgg(fig1, master=canvas_frame)
        canvas_widget1 = canvas1.get_tk_widget()
        canvas_widget1.grid(column=0, row=1)

        fig2 = show_spectrogram()
        canvas2 = FigureCanvasTkAgg(fig2, master=canvas_frame)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.grid(column=1, row=1)

        fig3 = unwrapped_phase_spectrum(state="max")
        canvas3 = FigureCanvasTkAgg(fig3, master=canvas_frame)
        canvas_widget3 = canvas3.get_tk_widget()
        canvas_widget3.grid(column=0, row=0, columnspan=3)

        fig4 = fourier_analysis()
        canvas4 = FigureCanvasTkAgg(fig4, master=canvas_frame)
        canvas_widget4 = canvas4.get_tk_widget()
        canvas_widget4.grid(column=2, row=1)

        canvas_widget1.bind('<Button-1>', on_canvas1_click)
        canvas_widget2.bind('<Button-1>', on_canvas2_click)
        canvas_widget3.bind('<Button-1>', on_canvas3_click)
        canvas_widget4.bind('<Button-1>', on_canvas4_click)

    elif main_element == "fourier_analysis":

        fig1 = wave_show()
        canvas1 = FigureCanvasTkAgg(fig1, master=canvas_frame)
        canvas_widget1 = canvas1.get_tk_widget()
        canvas_widget1.grid(column=0, row=1)

        fig2 = show_spectrogram()
        canvas2 = FigureCanvasTkAgg(fig2, master=canvas_frame)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.grid(column=1, row=1)

        fig3 = unwrapped_phase_spectrum()
        canvas3 = FigureCanvasTkAgg(fig3, master=canvas_frame)
        canvas_widget3 = canvas3.get_tk_widget()
        canvas_widget3.grid(column=2, row=1)

        fig4 = fourier_analysis(state="max")
        canvas4 = FigureCanvasTkAgg(fig4, master=canvas_frame)
        canvas_widget4 = canvas4.get_tk_widget()
        canvas_widget4.grid(column=0, row=0, columnspan=3)

        canvas_widget1.bind('<Button-1>', on_canvas1_click)
        canvas_widget2.bind('<Button-1>', on_canvas2_click)
        canvas_widget3.bind('<Button-1>', on_canvas3_click)
        canvas_widget4.bind('<Button-1>', on_canvas4_click)

    canvas_frame.grid(column=0, row=0)


def on_canvas1_click(event):
    create_canvas("wave_show")


def on_canvas2_click(event):
    create_canvas("show_spectrogram")


def on_canvas3_click(event):
    create_canvas("unwrapped_phase_spectrum")


def on_canvas4_click(event):
    create_canvas("fourier_analysis")


master = Tk()
starter_frame = Frame(master, background='black')
main_frame = Frame(master, background='white')
starter_frame.pack()

master.title('Audio analyser')

center_window(master, 1200, 650)
master.configure(background='black')

timer_label = Label(starter_frame, bd=0, font=("Times New Roman", 20), bg="black", fg="white")
button = Button(starter_frame, text="Record my voice", command=on_button_click, bg="white", fg="black", font=("Times New Roman", 20, "bold"), padx=30, pady=15)
progress = Progressbar(starter_frame, orient=HORIZONTAL, length=200, mode='determinate')

button.grid(column=0, row=3)
show_gif()

canvas_frame = Frame(main_frame, background='white')

changes_frame = Frame(main_frame, background='white')
master.mainloop()
