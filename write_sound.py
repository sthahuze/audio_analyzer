import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(filename='temp.wav', duration=5, sample_rate=44100):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()

    scaled_recording = recording.flatten()
    write(filename, sample_rate, scaled_recording)

