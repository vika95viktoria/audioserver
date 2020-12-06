from pydub import AudioSegment
import wave


def convert_to_wav(file_path, file_name):
    sound = AudioSegment.from_mp3(file_path)
    wav_file_name = f"{file_name}.wav"
    sound.export(wav_file_name, format="wav")
    return wave.open(wav_file_name).getnchannels()
