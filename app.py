from tkinter import *
from PIL import Image, ImageTk, ImageSequence


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
    gif_image = Image.open("audio_wave.gif")
    gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif_image)]

    gif_label = Label(master, bd=0)
    gif_label.pack()
    update_gif(0, gif_frames, gif_label)


master = Tk()
master.title('Counting Seconds')

# Центрування вікна
center_window(master, 1200, 650)
master.configure(background='black')

button = Button(master, text='Record my voice')
button.pack()

show_gif()

master.mainloop()
