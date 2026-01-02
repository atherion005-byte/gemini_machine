from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, AudioFileClip
from moviepy.config import change_settings

# --- CRITICAL FIX: HARDCODE THE PATH ---
# Go to C:\Program Files and find your ImageMagick folder name.
# Update the version number below if yours is different.
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

def generate_video_file(script_text, audio_file):
    print("    [+] Rendering visual cortex...")
    
    # 1. Load Audio to get exact duration
    audio = AudioFileClip(audio_file)
    
    # 2. Black Background (9:16 aspect ratio)
    bg = ColorClip(size=(1080, 1920), color=(0,0,0), duration=audio.duration)
    
    # 3. The Text Overlay
    # We use 'caption' method to auto-wrap text
    txt = TextClip(script_text, fontsize=70, color='white', font='Arial-Bold', 
                   size=(900, 1600), method='caption', align='center')
    txt = txt.set_position('center').set_duration(audio.duration)
    
    # 4. Combine
    final_video = CompositeVideoClip([bg, txt]).set_audio(audio)
    
    # 5. Export
    # We create a safe filename based on the audio name
    output_name = audio_file.replace("audio", "video").replace(".mp3", ".mp4")
    final_video.write_videofile(output_name, fps=24, codec='libx264', audio_codec='aac')
    
    return output_name