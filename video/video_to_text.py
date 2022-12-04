import moviepy.editor as mp
import os
import subprocess

from google.cloud import speech
from google.cloud import storage
import io
import whisper
import time

import argparse
import pathlib
import requests
import pathvalidate
import moviepy.editor as mp
import os
import subprocess
import whisper

ORIGIN = 'https://tube.switch.ch'

def video_to_audio(path):
    print("Opening path: ", path)
    # Convert video to audio
    clip = mp.VideoFileClip(path)
    #'.mp4'
    audio_name = path[:-4]+".mp3"
    print("Saving audio to", audio_name)
    clip.audio.write_audiofile(audio_name)

    # delete video since we no longer need it
    os.remove(path)

def compress_audio(path):
    output_ext = "flac"
    filename, ext = os.path.splitext(path)
    compressed = filename + "-compressed"
    subprocess.call(["lame", "-b", "32", path, f"{compressed}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    os.remove(path)


class GoogleAudio():
    def __init__(self):
        #setting Google credential
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./google_key.json"
        self.client = speech.SpeechClient.from_service_account_json('./google_key.json')
        self.storage_client = storage.Client()


    def speech_to_audio(self, path, bucket):

        filename, ext = os.path.splitext(path)
        gcs_uri = "gs://" + bucket + "/" + filename

        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            # encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            # sample_rate_hertz=24000,
            language_code="en-US",
            enable_word_time_offsets=True,
        )

        operation = self.client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=10000)

        transcript = ''
        ## TODO: PRODUCE OUTPUT TEXT
        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            transcript = result.alternatives[0].transcript
            # print(u"Transcript: {}".format(result.alternatives[0].transcript))
            # print("Confidence: {}".format(result.alternatives[0].confidence))
        print(transcript)
    def upload_file(self, path, bucket_name):
        bucket = self.storage_client.bucket(bucket_name)
        filename, ext = os.path.splitext(path)
        blob = bucket.blob(filename)

        blob.upload_from_filename(path)

        print(
            f"File {path} uploaded to {filename}."
        )


# gAudio = GoogleAudio()
# # gAudio.upload_file("downloads/01c1a2e5-CS-451  Week 1 Introduction-compressed.flac", "ginas_boys_buckets")
# gAudio.speech_to_audio("downloads/01c1a2e5-CS-451  Week 1 Introduction-compressed.flac", "ginas_boys_buckets")




class WhisperAnalysis():
    def __init__(self):
        self.model = whisper.load_model("base")
        print("whisp Init done")

    def transcribe(self, path):
        result = self.model.transcribe(path)
        return result

whisp = WhisperAnalysis()

# t = time.time()
print(whisp.transcribe("downloads/test-audio.flac"))
# print("took:", time.time() -t)
def get(url):
    """Return response data and URL for the next page given a URL.

    The returned URL will be `None` when there is no next page.
    """
    # Build the auth header using the access token command line argument.
    headers = {'Authorization': 'Token ' + 'token here}'}
    # GET from the URL. Include the auth header with the request.
    response = requests.get(url, headers=headers)
    # Stop and show a message when the response has an error status code.
    response.raise_for_status()
    # Try to get a the link to the next page.
    next_link = response.links.get('next')
    # Return the decoded data and a URL for the next page (if available).
    return (response.json(), next_link and next_link.get('url'))

def textified_from_url(video_id):
    url = ORIGIN + \
            '/api/v1/videos/{}'.format(video_id)
    response = get(url)
    print(response)

# textified_from_url('01c1a2e5')
# compress_audio("downloads/01c1a2e5-CS-451  Week 1 Introduction.mp3")