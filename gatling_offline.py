import time
import os
import PIL.Image

# --- COMPATIBILITY PATCHES ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})
# -----------------------------

from free_voice import generate_audio
from imagen_brain import generate_visual_asset 
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip

# --- DR. X HARDCODED AMMUNITION ---
# We bypass the API rate limits by providing the scripts manually.
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
    print("    [4] Merging Audio, Visual, and Captions...")
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    if visual_path and os.path.exists(visual_path):
        bg_clip = ImageClip(visual_path).set_duration(duration)
        bg_clip = bg_clip.resize(height=1920)
        bg_clip = bg_clip.set_position("center")
    else:
        print("    [!] Visual missing. Using fallback darkness.")
        bg_clip = ColorClip(size=(1080, 1920), color=(0,0,0), duration=duration)

    try:
        txt = TextClip(script_text, fontsize=60, color='white', font='Arial-Bold', 
                       size=(900, 1600), method='caption', align='center')
        txt = txt.set_position('center').set_duration(duration)
        final_video = CompositeVideoClip([bg_clip, txt])
    except Exception as e:
        print(f"    [!] Caption error: {e}. Exporting raw visual+audio.")
        final_video = bg_clip
    
    final_video = final_video.set_audio(audio)
    final_video.write_videofile(output_name, fps=24, codec='libx264', audio_codec='aac')
    print(f"    [+] WEAPON READY: {output_name}")

def ENGAGE():
    print("--- GATLING GUN (OFFLINE MODE) ONLINE ---")
    
    for i, round_data in enumerate(ROUNDS):
        topic = round_data["topic"]
        script = round_data["script"]
        
        print(f"\n[Target {i+1}/{len(ROUNDS)}]: {topic}")
        
        # 1. Intelligence (SKIPPED - USING MANUAL AMMO)
        print("    [1] Loading Hardcoded Script...")
        
        # 2. Voice
        audio_file = generate_audio(script, index=i)
        
        # 3. Vision (Using API only for this!)
        # We assume imagen_brain.py is correctly set to 'gemini-2.5-flash-image' from previous fix
        visual_file = generate_visual_asset(topic, index=i)
        
        # 4. Assembly
        output = f"FINAL_UPLOAD_{i}_{topic.replace(' ', '_')}.mp4"
        ASSEMBLE_WEAPON(script, audio_file, visual_file, output)
            
        print("    [~] Cooling down (5s)...")
        time.sleep(5)

if __name__ == "__main__":
    ENGAGE()