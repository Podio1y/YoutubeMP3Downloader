from pytube import YouTube
from pydub import AudioSegment
import os
import re

# Stores whether the user wants to exit or not
exit = "0"

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

# Removes any bad characters so that it does not search for an incorrect file name.
# Windows will remove all non-alpanumerical characters from a file name.
# Might improve by making it only include alphanumerical characters, rather then 
# just removing those 8 specific common ones.
def removeBadChars(name):
    # Removes all banned characters for windows file names
    bad_chars = "./\:*?\"<>|"
    for i in bad_chars:
        name = name.replace(i, "");
    
    return name

    # ALTERNATIVE METHOD with selected allowed characters instead
    # alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -_"
    # for i in name:
    #     if (i not in alphabet):
    #         name = name.replace(i, "")
    
    # return name


# Allows user to download songs repeatedly
while ((exit != 'x') & (exit != 'X')):
    # User inputs youtube url
    url = input(" Paste in your youtube url: ")
    video = YouTube(url)

    print(video.title)

    print(" Downloading Highest Quality Audio...")

    # Set the stream resolution to the best audio quality
    audio = video.streams.get_by_itag(get_best_audio())

    # Download it
    audio.download()

    print (" ")
    print (" Downloaded Successfully...")

    print (" ")
    print (" Converting to mp3...")

    cleansed_title = removeBadChars(audio.title)
    audio_file_name = cleansed_title + ".webm"
    converted_audio_file_name = cleansed_title + ".mp3"

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
    exit = input(" Done. Enter [x] to exit, or anything else to download another...")