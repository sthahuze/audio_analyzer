import librosa as lr
import numpy as np
from scipy.signal import spectrogram
from matplotlib.figure import Figure


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
    frequencies = np.fft.fftfreq(len(fourier_transform), 1/sample_rate)
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

