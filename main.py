import spotify
import downloadYT
import editing
import os

def karaoke_with_clip(token, song_name):
    print('Getting lyrics from the spotify API...')
    song = spotify.get_song_by_name(token, song_name)[0]
    subtitles = spotify.get_songs_subtitles(song['id'])['lines']
    print('---------------------------------------\n')
    
    print('Downloading...')
    videoID = downloadYT.searchVideo(song_name)
    downloadYT.downloadVideo("https://www.youtube.com/watch?v=" + videoID)
    print('---------------------------------------\n')
    
    print('Editing...')
    editing.add_subtitles_to_clip(subtitles, videoID + '.mp4')
    print(f'Done ! Check the file named {videoID}.mp4 in the output folder')
    
    #Clean it up
    os.remove('./videos/' + videoID + '.mp4')

if __name__ == '__main__':
    token = spotify.get_token()
    
    song_name = input('What song ? : ')
    
    karaoke_with_clip(token, song_name)