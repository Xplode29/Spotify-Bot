from __future__ import unicode_literals
import urllib.request
import re
from yt_dlp import YoutubeDL

VIDEO_SAVE_DIRECTORY = "./videos"
AUDIO_SAVE_DIRECTORY = "./audios"

def searchVideo(video_name):
    search = '+'.join(video_name.lower().split())
    
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={search}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    return video_ids[0]
    
def downloadAudio(url):
    soudsOpts = {
        'format': 'bestaudio/best', 
        'outtmpl': 'audios/%(id)s.mp3', 
        'noplaylist' : True, 
    }
    with YoutubeDL(soudsOpts) as ydl:
        ydl.download(url)

def downloadVideo(url):
    videoOpts = {
        'outtmpl': 'videos/%(id)s.mp4', 
        'noplaylist' : True, 
    }
    with YoutubeDL(videoOpts) as ydl:
        ydl.download(url)