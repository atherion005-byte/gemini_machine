import time
import os
import PIL.Image

# --- COMPATIBILITY PATCHES ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})
# -----------------------------

from gemini_brain import get_viral_script
from free_voice import generate_audio
from imagen_brain import generate_visual_asset 
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip

TOPICS = [
    "The Dead Internet Theory",
    "Roko's Basilisk",
    "Neuralink Glitch"
]

def ASSEMBLE_WEAPON(script_path, audio_path, visual_path, output_name):
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
        with open(script_path, "r") as f: raw_text = f.read()
        txt = TextClip(raw_text, fontsize=60, color='white', font='Arial-Bold', 
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
    print("--- HYBRID GATLING GUN (STABILIZED) ONLINE ---")
    
    for i, topic in enumerate(TOPICS):
        print(f"\n[Target {i+1}/{len(TOPICS)}]: {topic}")
        
        # 1. Intelligence
        script_text = get_viral_script(topic)
        
        # Check if the brain failed
        if "System Error" in script_text:
            print("    [!] Brain offline. Skipping round.")
            time.sleep(10)
            continue

        script_file = f"script_{i}.txt"
        with open(script_file, "w") as f: f.write(script_text)
        
        # 2. Voice
        audio_file = generate_audio(script_text, index=i)
        
        # 3. Vision
        visual_file = generate_visual_asset(topic, index=i)
        
        # 4. Assembly
        output = f"FINAL_UPLOAD_{i}_{topic.replace(' ', '_')}.mp4"
        ASSEMBLE_WEAPON(script_file, audio_file, visual_file, output)
            
        print("    [~] Cooling down barrels (20s)...") # Increased cooldown
        time.sleep(20)

if __name__ == "__main__":
    ENGAGE()