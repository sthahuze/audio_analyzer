import numpy as np
import soundfile as sf


def apply_hall(signal, delay_first_repeat=0.1, num_repeats=10):
    num_samples = len(signal)
    sample_rate = 44100
    delay_samples = int(delay_first_repeat * sample_rate)

    hall = np.zeros(num_samples + delay_samples * num_repeats)

    for i in range(num_repeats):
        start_idx = i * delay_samples
        end_idx = start_idx + num_samples
        hall[start_idx:end_idx] += signal * (1 - i / num_repeats)

    hall = hall[:num_samples]

    return signal + hall


signal, sampling_frequency = sf.read('temp.wav')
signal_with_hall = apply_hall(signal, delay_first_repeat=0.1, num_repeats=10)

sf.write('output.wav', signal_with_hall, sampling_frequency)
