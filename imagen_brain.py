from google import genai
from google.genai import types
import os

# --- DR. X VISUAL SHOTGUN PROTOCOL ---
API_KEY = "AIzaSyCA-gkmoVfyiizE2cwgFT5xRTAtws525FU"
client = genai.Client(api_key=API_KEY)

# The Kill List: We try these models in order until one works.
TARGET_MODELS = [
    "models/imagen-3.0-generate-001",          # The Heavy Artillery (Standard)
    "models/gemini-2.0-flash",                 # The Multimodal Beast
    "models/gemini-2.5-flash-image",           # The Specialist
    "models/gemini-2.5-flash-image-preview",   # The Prototype
    "models/image-generation-001"              # The Legacy Fallback
]

def generate_visual_asset(topic, index=1):
    print(f"    [>>>] ENGAGING VISUAL SHOTGUN FOR: '{topic}'")
    
    prompt_text = f"A dark, cinematic, photorealistic vertical poster about {topic}. 9:16 aspect ratio. Cyberpunk horror aesthetic. High contrast. 8k resolution."
    
    for model_id in TARGET_MODELS:
        print(f"        [?] Testing barrel: {model_id}...")
        try:
            # Fire the request
            response = client.models.generate_images(
                model=model_id, 
                prompt=prompt_text,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="9:16"
                )
            )
            
            if response.generated_images:
                image = response.generated_images[0]
                filename = f"VISUAL_BG_{index}.png" 
                print(f"    [+] TARGET HIT with {model_id}. Visual secured: {filename}")
                image.image.save(filename)
                return filename
            
        except Exception as e:
            # If it fails, we just log it and move to the next barrel
            clean_error = str(e).split('message')[0][:100] # Keep logs clean
            print(f"        [x] Jammed ({clean_error}...). Cycling...")
            continue

    print("    [!] CRITICAL FAILURE: All barrels empty. Visual generation failed.")
    return None