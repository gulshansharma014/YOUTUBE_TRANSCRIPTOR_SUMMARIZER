from youtube_dl import YoutubeDL
from pydub import AudioSegment
# from pytube import YouTube
import speech_recognition as sr
from os import path


# from huggingsound import SpeechRecognitionModel
# import librosa
# import soundfile as sf
#
def getaudio(video_id):
    URL = f"https://www.youtube.com/watch?v={video_id}"
    print(URL)
    audio = YoutubeDL({'format': 'bestaudio'})
    print(audio, "line16")
    details = audio.extract_info(URL, download=True)
    print(details, "line18")
    sound = AudioSegment.from_mp3("transcript.mp3")
    sound.export("transcript.wav", format="wav")

    # transcribe audio file
    AUDIO_FILE = "transcript.wav"

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
        print("Transcription: " + r.recognize_google(audio))
    #     # return r.recognize_google(audio)

    print(details)
    #
    #     yt = YouTube(URL)
    #     yt.streams \
    #         .filter(only_audio=True, file_extension='mp4') \
    #         .first() \
    #         .download(filename='ytaudio.mp4') \
    #
    #     ffmpeg - i ytaudio.mp4 - acodec
    #     pcm_s16le - ar
    #     16000
    #     ytaudio.wav
    #
    #     model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english", device=device)
    #
    #     input_file = '/content/ytaudio.wav'
    #     print(librosa.get_samplerate(input_file))
    #
    #     # Stream over 30 seconds chunks rather than load the full file
    #     stream = librosa.stream(
    #         input_file,
    #         block_length=30,
    #         frame_length=16000,
    #         hop_length=16000
    #     )
    #     for i, speech in enumerate(stream):
    #         sf.write(f'{i}.wav', speech, 16000)
    #
    #     audio_path = []
    #     for a in range(i + 1):
    #         audio_path.append(f'/content/{a}.wav')
    #
    #     transcriptions = model.transcribe(audio_path)
    #     full_transcript = ' '
    #     for item in transcriptions:
    #         full_transcript += ''.join(item['transcription'])
    #
    # return full_transcript
