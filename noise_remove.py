import sounddevice as sd
from scipy.io.wavfile import read, write
import noisereduce as nr


# працює, але дивно
rate, data = read("temp.wav")

reduced_noise = nr.reduce_noise(y=data, sr=rate)
write('output.wav', rate, reduced_noise)

