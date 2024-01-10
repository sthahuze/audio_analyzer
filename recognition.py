import speech_recognition as sr
from pydub import AudioSegment


def recognize_speech_from_audio(audio_file):
    recognizer = sr.Recognizer()

    audio = AudioSegment.from_file(audio_file)
    audio.export(audio_file, format="wav")

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


