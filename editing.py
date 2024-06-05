# Import everything needed to edit video clips
import moviepy.editor as edit

def add_subtitles_to_clip(subtitles, video_name):
    baseVideo = edit.VideoFileClip('./videos/' + video_name)
    
    all_clips = []
    
    for index in range(len(subtitles) - 1):
        timeCode = int(subtitles[index]['startTimeMs']) / 1000
        nextTimeCode = int(subtitles[index + 1]['startTimeMs']) / 1000
        if index >= len(subtitles) - 1:
            nextTimeCode = baseVideo.duration
        
        words = subtitles[index]['words']
        if words == '': words = '♪'
        
        txt_clip = edit.TextClip(
            txt = str(words), 
            font = 'Arial Bold',
            fontsize = 40, 
            color = 'white', 
            stroke_color = 'white', 
            stroke_width = 5
        )
        
        txt_clip = txt_clip.set_duration(nextTimeCode - timeCode)
        
        all_clips.append(txt_clip)
    
    text_overlay = edit.concatenate_videoclips(clips = all_clips).set_start(int(subtitles[0]['startTimeMs']) / 1000).set_pos('center')
    
    video = edit.CompositeVideoClip([baseVideo, text_overlay])
    video.write_videofile('./output/' + video_name)