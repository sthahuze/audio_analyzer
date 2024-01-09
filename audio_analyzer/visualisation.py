import librosa as lr
import matplotlib.pyplot as plt
import numpy as np

# Load the audio recording
audio_data, sample_rate = lr.load("audio_recording.wav")
lr.display.waveshow(audio_data, sr=sample_rate, color="b")

# Display the waveform of the audio signal
plt.title('Waveform of Audio Signal (Volume)')
plt.xlabel('Time (s)')
plt.show()

# Perform Fourier transform on the audio signal
fourier_transform = np.fft.fft(audio_data)
frequencies = np.fft.fftfreq(len(fourier_transform), 1/sample_rate)
amplitudes = np.abs(fourier_transform)

# Plot the Fourier analysis
plt.figure(figsize=(10, 4))
plt.plot(frequencies, amplitudes)
plt.title('Fourier Analysis')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Create a time array for the audio signal
time = np.arange(0, len(audio_data)) / sample_rate

# Plot the audio signal in the time domain
plt.figure(figsize=(10, 4))
plt.plot(time, audio_data)
plt.title('Audio Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Compute and display the spectrogram of the audio signal
from scipy.signal import spectrogram
f, t, Sxx = spectrogram(audio_data, sample_rate)
plt.pcolormesh(t, f, 10 * np.log10(Sxx))
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.title('Spectrogram')
plt.show()

# Analyze the phase information of the Fourier transform
phases = np.angle(fourier_transform)
phases_unwrapped = np.unwrap(phases)

# Plot the unwrapped phase spectrum
plt.figure(figsize=(10, 4))
plt.plot(frequencies, phases_unwrapped)
plt.title('Unwrapped Phase Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase')
plt.show()
