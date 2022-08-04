from pytube import YouTube
from pydub import AudioSegment
import os

# User inputs youtube url
url = input(" Paste in your youtube url: ")
video = YouTube(url)

print(video.title)

print(" Downloading Highest Quality Audio...")

# Finds and returns the itag corresponding to the best audio 
# quality file from the youtube API
def get_best_audio():
    previous_quality = int(0)

    # Iterates through every audio-only quality option and finds the best
    for stream in video.streams.filter(only_audio = True):

        # Removes the Kbps from the end of the string and casts to int
        current_quality = int( stream.abr[0:(len(stream.abr)-4)])
        
        # If the current quality is better, set this to the new best audio
        if ( current_quality > previous_quality):
            best_audio_tag = stream.itag
            previous_quality = current_quality
    
    return best_audio_tag


# Set the stream resolution to the best audio quality
audio = video.streams.get_by_itag(get_best_audio())

# Download it
audio.download()

print (" ")
print (" Downloaded Successfully...")

print (" ")
print (" Converting to mp3...")

audio_file_name = audio.title + ".webm"
converted_audio_file_name = audio.title + ".mp3"

# Convert the webm file to mp3
mp3_audio = AudioSegment.from_file(audio_file_name)#, format="webm")
mp3_audio.export(converted_audio_file_name, format="mp3")

print (" ")
print (" Converted Successfully...")

print (" ")
print (" Removing Original webm file...")

# Removing the webm file after generating the mp3
if (os.path.exists(audio_file_name)):
    os.remove(audio_file_name)
    print (" Removed Successfully")
else:
    print (" Could not remove webm file...")

print(" ")
input(" Done. Enter any key to close")