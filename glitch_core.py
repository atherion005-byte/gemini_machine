import numpy as np
import random
import os
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, ImageClip
import PIL.Image

# --- COMPATIBILITY PATCH ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.config import change_settings
# Ensure this path matches your system
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

def make_glitch_frame(t):
    # Generates random static noise
    # We create a small array and scale it up to look like blocky digital noise
    w, h = 270, 480 # Low res for blocky effect
    frame = np.random.randint(0, 255, (h, w, 3)).astype('uint8')
    return frame

def generate_digital_decay(topic, duration=5, index=0):
    print(f"    [>>>] GENERATING DIGITAL DECAY FOR: '{topic}'")
    
    # 1. Base Layer: Black
    bg = ColorClip(size=(1080, 1920), color=(0,0,0), duration=duration)
    
    # 2. The Glitch Layers
    # We create random red/white flashes
    clips = [bg]
    
    for _ in range(5):
        # Random flash of red or white
        color = random.choice([(255,0,0), (255,255,255), (50,50,50)])
        start = random.uniform(0, duration)
        length = random.uniform(0.1, 0.3)
        flash = ColorClip(size=(1080, 1920), color=color, duration=length).set_start(start).set_opacity(0.3)
        clips.append(flash)

    # 3. The Text Layer (System Warnings)
    warnings = ["SYSTEM_FAILURE", "NO_SIGNAL", "REDACTED", "404_REALITY", topic.upper().replace(" ", "_")]
    
    for _ in range(3):
        word = random.choice(warnings)
        txt = TextClip(word, fontsize=100, color='red', font='Courier', method='label')
        
        # Random position
        x = random.randint(100, 800)
        y = random.randint(200, 1600)
        
        start = random.uniform(0, duration)
        length = random.uniform(0.5, 1.0)
        
        txt_clip = txt.set_position((x,y)).set_start(start).set_duration(length)
        clips.append(txt_clip)

    # 4. Composite
    final_glitch = CompositeVideoClip(clips)
    
    filename = f"GLITCH_BG_{index}.mp4"
    # We write a temp file to lock it in
    final_glitch.write_videofile(filename, fps=10, codec='libx264', preset='ultrafast', logger=None)
    
    print(f"    [+] Decay generated: {filename}")
    return filename

if __name__ == "__main__":
    generate_digital_decay("TEST_SIGNAL")