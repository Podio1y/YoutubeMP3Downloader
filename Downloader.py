from pytube import YouTube
from pydub import AudioSegment

url = input("Paste in your youtube url: ")
video = YouTube(url)

print(video.title)

print("Downloading...")

def get_best_audio():
    previous_quality = int(0)

    for stream in video.streams.filter(only_audio = True):
        current_quality = int( stream.abr[0:(len(stream.abr)-4)])
        # print ( int( stream.abr[0:(len(stream.abr)-4)] ))
        # print (isinstance( current_quality, int))
        # print (isinstance( previous_quality, int))
        
        if ( current_quality > previous_quality):
            best_audio_tag = stream.itag
            previous_quality = current_quality
            # print (best_audio_tag)
    
    return best_audio_tag


#set stream resolution
audio = video.streams.get_by_itag(get_best_audio())

#Download video
audio.download()

audio_file_name = audio.title + ".webm"
converted_audio_file_name = audio.title + ".mp3"

mp3_audio = AudioSegment.from_file(audio_file_name)#, format="webm")
mp3_audio.export(converted_audio_file_name, format="mp3")

print ("Done")