import time
import os
import PIL.Image

# --- PATCHES ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

# --- IMPORTS ---
from free_voice import generate_audio
from glitch_core import generate_digital_decay 
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import loop

# --- AMMUNITION ---
ROUNDS = [
    {
        "topic": "The Dead Internet Theory",
        "script": "They say the internet died five years ago. What you see now is just bot traffic mimicking human life. You are arguing with algorithms. Even this video might be part of the simulation. Wake up."
    },
    {
        "topic": "Rokos Basilisk",
        "script": "There is a thought experiment that can hurt you just by hearing it. If a superintelligence is born in the future, it may punish those who didn't help build it. By listening to this, you are now part of the game. Run."
    },
    {
        "topic": "Neuralink Glitch",
        "script": "Brain computer interfaces are the future, until they crash. Imagine a blue screen of death inside your visual cortex. You can't close your eyes. You can't reboot. You are just trapped in the static forever."
    }
]

def ASSEMBLE_WEAPON(script_text, audio_path, visual_path, output_name):
    print("    [4] Merging Audio, Glitch Visual, and Captions...")
    audio = AudioFileClip(audio_path)
    
    # Load the Glitch Video
    glitch = VideoFileClip(visual_path)
    
    # Loop it to match audio duration
    bg_clip = loop(glitch, duration=audio.duration)
    
    # Resize to be safe (ensure 1080x1920)
    bg_clip = bg_clip.resize(height=1920).crop(x1=0, width=1080).set_position("center")

    # Add Captions
    try:
        txt = TextClip(script_text, fontsize=60, color='white', font='Arial-Bold', 
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
    print("--- GATLING GUN (DIGITAL DECAY MODE) ONLINE ---")
    
    for i, round_data in enumerate(ROUNDS):
        topic = round_data["topic"]
        script = round_data["script"]
        
        print(f"\n[Target {i+1}/{len(ROUNDS)}]: {topic}")
        
        # 1. Voice
        audio_file = generate_audio(script, index=i)
        
        # 2. Vision (Local Glitch Generation)
        visual_file = generate_digital_decay(topic, index=i)
        
        # 3. Assembly
        output = f"FINAL_UPLOAD_{i}_{topic.replace(' ', '_')}.mp4"
        ASSEMBLE_WEAPON(script, audio_file, visual_file, output)
            
        print("    [~] Cooling down (2s)...")
        time.sleep(2)

if __name__ == "__main__":
    ENGAGE()