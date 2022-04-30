from flask import Flask, render_template, url_for, request, redirect
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from transformers import pipeline
from test import getaudio
from translate import g_translate
import json
from flask import send_from_directory
import os


def getTranscript(video_id):
    # YouTubeTranscriptApi.get_transcript(video_id, languages=['de', 'en'])
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['de', 'en'])

    formatter = JSONFormatter()


    json_formatted = formatter.format_transcript(transcript)

    result = ""
    for i in transcript:
        result += ' ' + i['text']

    return result


def getSummary(full_transcript):
    summarizer = pipeline("summarization")
    # summary = summarizer(article)[0]['summary']
    num_iters = int(len(full_transcript) / 1000)
    summarized_text = ""
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        # print("input text \n" + full_transcript[start:end])
        out = summarizer(full_transcript[start:end], min_length=5, max_length=20)
        out = out[0]
        out = out['summary_text']
        # print("Summarized text\n"+out)
        summarized_text += out

    return summarized_text


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index_page():
    if request.method == 'POST':
        youtube_video = str(request.form['content'])
        language = str(request.form['lang'])

        if (youtube_video == ""):
            return redirect('/')

        video_id = youtube_video.split("=")[1]

        try:
            transcript = getTranscript(video_id)
            print(transcript)

        except:
            try:
                transcript = getaudio(video_id)

            except:
                return "There was a problem getting the Transcript"

        '''if language == 'Hindi':
            final_transcript = g_translate(transcript, 'hi')

        elif language == 'Gujrati':
            final_transcript = g_translate(transcript, 'gu')

        else :
            final_transcript = g_translate(transcript, 'en')'''
        ttranscript = getSummary(transcript);
        print(ttranscript)
        final_transcript = g_translate(ttranscript, language)
        print(final_transcript)

        return render_template('index.html', summary=final_transcript)

    else:
        return render_template('index.html')



# app.route('/time', methods=['GET'])
# def get_time():

# server the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)