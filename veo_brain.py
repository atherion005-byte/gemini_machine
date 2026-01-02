from google import genai
from google.genai import types
import time
import os

# --- DR. X VEO 3.1 PROTOCOL ---
# PASTE YOUR KEY HERE.
API_KEY = "AIzaSyCA-gkmoVfyiizE2cwgFT5xRTAtws525FU"

client = genai.Client(api_key=API_KEY)

def generate_veo_asset(topic, index=1):
    print(f"    [>>>] ENGAGING VEO 3.1 CORE FOR: '{topic}'")
    
    # Dr. X Prompt Engineering: We explicitly ask for audio in the prompt
    prompt_text = (
        f"A cinematic, hyper-realistic, dark techno-thriller vertical video about {topic}. "
        "Cyberpunk atmosphere. 4k resolution. "
        "Soundtrack: Dark ambient drone, glitch noises, cybernetic hum, scary industrial sounds."
    )
    
    try:
        print("    [1] Transmitting payload to Google Cloud...")
        
        # TARGET LOCKED: veo-3.1-generate-preview
        # REMOVED: generate_audio=True (This caused your crash. The model does it automatically based on prompt.)
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt_text,
            config=types.GenerateVideosConfig(
                aspect_ratio="9:16",
                duration_seconds=6  # Maximize the duration
            )
        )
        
        print("    [~] Rendering (This takes time, do not close)...")
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation)
            print("        ...processing...")
            
        if operation.result and operation.result.generated_videos:
            video_asset = operation.result.generated_videos[0]
            filename = f"VEO_UPLOAD_{index}_{topic.replace(' ', '_')}.mp4"
            
            print(f"    [+] VEO ASSET SECURED: {filename}")
            video_asset.video.save(filename)
            return filename
        else:
            print("    [!] VEO FAILURE: No video returned.")
            return None

    except Exception as e:
        print(f"    [!] CRITICAL ERROR: {e}")
        return None