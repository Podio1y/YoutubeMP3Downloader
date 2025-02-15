# from pytube import YouTube
from pytubefix import YouTube
from pydub import AudioSegment
from pathlib import Path
import os
import re
import shutil
import requests
import glob

import eyed3
from eyed3.id3.frames import ImageFrame

# Stores whether the user wants to exit or not
exit = "0"

def get_thumbnail(video, cleansed_title):
    img = requests.get(video.thumbnail_url).content
    thumbnail_name = cleansed_title + ".jpg"
    with open(thumbnail_name, 'wb') as handler:
        handler.write(img)

    return thumbnail_name

# Finds and returns the itag corresponding to the best audio 
# quality file from the youtube API
def get_best_audio(video):
    previous_quality = int(0)

    # Iterates through every audio-only quality option and finds the best
    for stream in video.streams.filter(only_audio = True):

        # Removes the Kbps from the end of the string and casts to int
        if (stream.abr == None):
            continue

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
    f = open("badchars.txt", "r")
    # bad_chars = "./\:*?\"<>|',"
    bad_chars = f.readline()
    for i in bad_chars:
        name = name.replace(i, "");
    
    f.close()

    return name

    # ALTERNATIVE METHOD with selected allowed characters instead
    # alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -_"
    # for i in name:
    #     if (i not in alphabet):
    #         name = name.replace(i, "")
    
    # return name

def add_bad_char(badchar):
    f = open("badchars.txt", "a")
    f.write(badchar)
    f.close()

def main():
    # os.system("cmd /k")
    exit = '.'
    # Allows user to download songs repeatedly
    while ((exit != 'x') & (exit != 'X')):
        # User inputs youtube url
        os.system("cls")
        url = input(" Paste in your youtube url: ")
        video = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        # video = YouTube(url)

        # print("Video: " + video.title + "\n")
        try:
            print("Video: " + video.title + "\n")
        except Exception as e:
            print("Error getting video title: " + str(e))
            input("press anything to restart.")
            continue

        print(" Downloading Highest Quality Audio...")

        best = get_best_audio(video)
        # print(best)

        # Set the stream resolution to the best audio quality
        try:
            audio = video.streams.get_by_itag(best)
        except Exception as e:
            print("ERROR: get_by_itag - " + str(e))
            input("Enter anything to exit.")
            quit()

        # Download it
        audio.download()

        print (" ")
        print (" Downloaded Successfully...")

        print (" ")
        print (" Converting to mp3...")

        cleansed_title = removeBadChars(audio.title)
        audio_file_name = cleansed_title + ".webm"
        audio_file_name_m4a = cleansed_title + ".m4a"
        converted_audio_file_name = cleansed_title + ".mp3"

        name_in_windows = glob.glob("*.m4a")[0]

        # Convert the webm file to mp3
        # mp3_audio = AudioSegment.from_file(audio_file_name)#, format="webm")
        mp3_audio = AudioSegment.from_file(name_in_windows)
        mp3_audio.export(converted_audio_file_name, format="mp3")

        print (" ")
        print (" Converted Successfully...")

        print (" ")
        print (" Removing Original file...")

        # Removing the webm file after generating the mp3
        if (os.path.exists(audio_file_name)):
            os.remove(audio_file_name)
            print (" Removed webm Successfully")
        else:
            print (" Could not remove webm file...")

        # print(name_in_windows)

        # Removing the webm file after generating the mp3
        if (os.path.exists(name_in_windows)):
            os.remove(name_in_windows)
            print (" Removed m4a Successfully")
        else:
            print (" Could not remove m4a file...")

        # Setting the songs thumbnail
        print(" ")
        print (" Getting the song thumbnail...")
        thumb_name = get_thumbnail(video, cleansed_title)

        audiofile = eyed3.load(converted_audio_file_name)
        audiofile.initTag(version=(2, 3, 0))

        print (" ")
        print (" Applying the thumbnail to the mp3...")
        audiofile.tag.images.set(3, open(thumb_name,"rb").read(), "image/jpeg", u"cover")

        audiofile.tag.save()
        print (" Applied Successfully")
        ######################

        # Removing the jpg file after adding it to the mp3
        print (" ")
        print (" Removing the thumbnail file...")
        if (os.path.exists(thumb_name)):
            os.remove(thumb_name)
            print (" Removed Successfully")
        else:
            print (" Could not remove thumbnail file...")
        
        # Moving the mp3 to music folder
        curPath = converted_audio_file_name
        desiredPath = "G:/YoutubeDL/" + converted_audio_file_name
        print(" ")
        print(" Moving MP3 to desired folder...")

        if (os.path.exists(converted_audio_file_name)):
            shutil.move(curPath, desiredPath)
            print(" Moved Successfully")
        else:
            print(" Could not move to the set directory: " + desiredPath)
        

        print(" ")
        exit = input(" Done. Enter [x] to exit, or anything else to download another...")

if __name__ == "__main__":
    main()