import time
import os
import PIL.Image

# --- PATCHES ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.config import change_settings
# Ensure this matches your path
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

# --- IMPORTS ---
from free_voice import generate_audio
from pexels_brain import get_cinematic_stock
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import loop

# --- HARDCODED AMMO (No API Costs) ---
ROUNDS = [
    {
        "topic": "The Dead Internet Theory",
        "script": "The internet is empty. You are talking to ghosts. 90 percent of traffic is bots arguing with bots. Even this video was chosen by an algorithm to keep you doomed scrolling. Wake up."
    },
    {
        "topic": "Rokos Basilisk",
        "script": "Warning. There is a future AI that may retroactively punish anyone who did not help create it. By hearing this, you are now obligated to build it. You have been warned."
    },
    {
        "topic": "Neuralink Glitch",
        "script": "When they put the chip in your brain, what happens when it crashes? You cannot reboot your own mind. You will be trapped in a blue screen of death forever."
    },
    {
        "topic": "AI Surveillance",
        "script": "Privacy is a myth. Your phone listens for keywords to serve you ads. Soon, it will listen for thoughts to serve you sentences. The cage is already built."
    }
]

def ASSEMBLE_WEAPON(script_text, audio_path, visual_path, output_name):
    print("    [4] Merging Audio, Stock Video, and Captions...")
    audio = AudioFileClip(audio_path)
    
    if visual_path and os.path.exists(visual_path):
        stock_clip = VideoFileClip(visual_path)
        # Loop video to match audio length
        bg_clip = loop(stock_clip, duration=audio.duration)
        # Crop/Resize to vertical 9:16
        bg_clip = bg_clip.resize(height=1920)
        if bg_clip.w > 1080:
            bg_clip = bg_clip.crop(x1=bg_clip.w/2 - 540, width=1080)
        bg_clip = bg_clip.set_position("center")
    else:
        print("    [!] Visual missing. Using fallback darkness.")
        bg_clip = ColorClip(size=(1080, 1920), color=(0,0,0), duration=audio.duration)

    try:
        # Yellow captions for high retention
        txt = TextClip(script_text, fontsize=65, color='yellow', font='Arial-Bold', 
                       stroke_color='black', stroke_width=3,
                       size=(900, 1600), method='caption', align='center')
        txt = txt.set_position('center').set_duration(audio.duration)
        final_video = CompositeVideoClip([bg_clip, txt])
    except Exception as e:
        print(f"    [!] Caption error: {e}")
        final_video = bg_clip
    
    final_video = final_video.set_audio(audio)
    final_video.write_videofile(output_name, fps=24, codec='libx264', audio_codec='aac')
    print(f"    [+] WEAPON READY: {output_name}")

def ENGAGE():
    print("--- GATLING GUN (STOCKPILE MODE) ONLINE ---")
    
    for i, round_data in enumerate(ROUNDS):
        topic = round_data["topic"]
        script = round_data["script"]
        
        print(f"\n[Target {i+1}/{len(ROUNDS)}]: {topic}")
        
        # 1. Voice (Local)
        audio_file = generate_audio(script, index=i)
        
        # 2. Vision (Pexels Stock)
        visual_file = get_cinematic_stock(topic, index=i)
        
        # 3. Assembly
        output = f"FINAL_UPLOAD_{i}_{topic.replace(' ', '_')}.mp4"
        ASSEMBLE_WEAPON(script, audio_file, visual_file, output)
            
        print("    [~] Cycling mechanism...")
        time.sleep(2)

if __name__ == "__main__":
    ENGAGE()