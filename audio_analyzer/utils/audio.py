import sounddevice as sd
import numpy as np
import scipy as sp
import speech_recognition as sr
from sklearn.preprocessing import StandardScaler
import librosa
import soundfile
import joblib


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


## Least Mean Squares noise cancellation filter
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


def reverb_filter(audio, delay, decay, decay_coef, repetitions):
    signal, sample_rate = audio
    delay_samples = int(delay * sample_rate)
    res = np.zeros(delay_samples * repetitions + signal.size)
    res[:signal.size] = signal

    for i in range(1, repetitions + 1):
        n = delay_samples * i
        d = (decay - decay_coef * i)
        if d <= 0: break
        res[n:signal.size + n] += d * signal

    return res, sample_rate


def band_filter(audio, low_freq, high_freq, order): 
    signal, sample_rate = audio
    b, a = sp.signal.butter(order, (low_freq, high_freq), btype='band', fs=sample_rate)
    res = sp.signal.lfilter(b, a, signal)
    return res, sample_rate


def distortion_filter(audio, coef=5., gain=1.):
    signal, sample_rate = audio
    res = np.tanh(coef * signal) / np.tanh(coef) * gain
    return res, sample_rate


def recognize_speech(audio):
    data, sample_rate = audio
    quant_data = np.int16((2**15 - 1) * data)
    recognizer = sr.Recognizer()

    segment = sr.AudioData(quant_data, sample_rate, quant_data.itemsize)

    try:
        text = recognizer.recognize_google(segment)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")



def extract_feature(audio, sample_rate, mfcc, chroma, mel):
    result = np.array([])
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        stft = np.abs(librosa.stft(audio))
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma))
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel))

    return result


def recognize_emotion(audio):
    signal, sample_rate = audio
    model = joblib.load('audio_analyzer/utils/model.joblib')
    features = extract_feature(signal, sample_rate, mfcc=True, chroma=True, mel=True).reshape(1, -1)
    scaler = StandardScaler()
    scaler.fit(features)
    scaled_features = scaler.transform(features)
    predicted_emotion = model.predict(scaled_features)

    return predicted_emotion
