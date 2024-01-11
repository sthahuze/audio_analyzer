import sounddevice as sd
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment


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


def lms_filter(audio, step_size, filter_order):
    signal_data, sample_rate = audio
    num_samples = len(signal_data)
    weights = np.zeros(filter_order)
    output_signal = np.zeros(num_samples)

    for i in range(filter_order, num_samples):
        input_vector = signal_data[i-filter_order:i]
        predicted_output = np.dot(weights, input_vector)
        error = signal_data[i] - predicted_output
        weights += 2 * step_size * error * input_vector
        output_signal[i] = predicted_output

    return output_signal, sample_rate


def recognize_speech(audio):
    data, sample_rate = audio
    recognizer = sr.Recognizer()

    segment = sr.AudioData(data, sample_rate, data.itemsize)

    try:
        text = recognizer.recognize_google(segment)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
