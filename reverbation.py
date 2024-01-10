import numpy as np
import soundfile as sf
from matplotlib.figure import Figure
from pydub import AudioSegment
from pydub.playback import play


def apply_hall(filename='temp.wav', delay_first_repeat=0.1, num_repeats=10):
    signal, sampling_frequency = sf.read(filename)
    num_samples = len(signal)
    sample_rate = 44100
    delay_samples = int(delay_first_repeat * sample_rate)

    hall = np.zeros(num_samples + delay_samples * num_repeats)

    for i in range(num_repeats):
        start_idx = i * delay_samples
        end_idx = start_idx + num_samples
        hall[start_idx:end_idx] += signal * (1 - i / num_repeats)

    hall = hall[:num_samples]
    signal_with_hall = signal + hall

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot()
    ax.set_title('Reverbed signal')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')

    ax.plot(np.arange(len(signal_with_hall)) / sampling_frequency, signal_with_hall)

    return signal_with_hall, fig


def play_audio(signal, sampling_frequency=44100):
    # Переконайтеся, що ширина зразка становить 16 біт
    if signal.dtype.itemsize != 2:
        signal = (signal * 32767).astype(np.int16)

    # Преобразуйте NumPy-масив у формат, який може використовувати pydub
    audio_segment = AudioSegment(
        signal.tobytes(),
        frame_rate=sampling_frequency,
        sample_width=2,  # Встановіть ширину зразка в 16 біт
        channels=1  # Моно аудіо
    )

    # Відтворення аудіосигналу
    play(audio_segment)
