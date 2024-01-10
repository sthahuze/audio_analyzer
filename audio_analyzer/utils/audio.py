import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write


def record_audio(duration=5, sample_rate=44100):
    recording = sd.rec(int(duration * sample_rate),
                       samplerate=sample_rate,
                       channels=1)
    sd.wait()

    scaled_recording = recording.flatten()
    return scaled_recording, sample_rate


def play_audio(audio):
    data, sample_rate = audio
    sd.play(data, sample_rate)
    sd.wait()


# def noise_cancel()
