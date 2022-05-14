from youtube_dl import YoutubeDL
from pydub import AudioSegment
from pytube import YouTube
import speech_recognition as sr
from os import path
import os
import librosa
import soundfile as sf
from huggingsound import SpeechRecognitionModel


def getaudio(video_id):
    URL = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(URL)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    # download audio from video
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
    # os.rename(yt.streams.first().default_filename, 'transcript.mp3')
    sound = AudioSegment.from_mp3("Animation Video (without subtitles)- Student Guidance & Counselling Services-aSdxFj1LqwY.mp3")

    # converting into wav format
    sound.export("transcript.wav", format="wav")

    # audio chunking
    input_file = 'transcript.wav'
    stream = librosa.stream(
        input_file,
        block_length=30,
        frame_length=16000,
        hop_length=16000
    )

    for i, speech in enumerate(stream):
        sf.write(f'{i}.wav', speech, 16000)
    print("audio start")

    audio_path = []
    for a in range(i + 1):
        audio_path.append(f'{a}.wav')
    print("audio_path", audio_path)

    # transcripting every chunk
    model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")
    print("model", model)
    transcriptions = model.transcribe('transcript.wav')
    print(transcriptions)

    # complete transcript
    full_transcript = ''
    for item in transcriptions:
        full_transcript += ''.join(item['transcription'])

    print(full_transcript)
    return full_transcript
