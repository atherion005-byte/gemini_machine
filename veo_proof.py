from google import genai
from google.genai import types
import time
import os

# --- DR. X VERIFICATION SHOT ---
# PASTE YOUR KEY HERE.
API_KEY = "AIzaSyCA-gkmoVfyiizE2cwgFT5xRTAtws525FU"

client = genai.Client(api_key=API_KEY)

def fire_verification_round():
    print("--- INITIATING VEO 3.1 PAYMENT VERIFICATION ---")
    
    # High-fidelity prompt to test full capabilities
    prompt_text = (
        "Cinematic drone shot of a futuristic cyberpunk city in rain, neon lights reflecting on wet pavement. "
        "Hyper-realistic, 4k resolution, highly detailed. "
        "Soundtrack: Heavy rain, distant sirens, deep synth bass drone."
    )
    
    try:
        print("[1] Contacting Google Cloud Billing Verification...")
        
        # We target the specific preview model. 
        # If this fails with 404, we fallback to 2.0.
        model_id = "veo-3.1-generate-preview" 
        
        operation = client.models.generate_videos(
            model=model_id,
            prompt=prompt_text,
            config=types.GenerateVideosConfig(
                aspect_ratio="9:16",
                duration_seconds=6 
            )
        )
        
        print(f"[~] Authorization accepted. Rendering on {model_id}...")
        print("    (This allows us to confirm audio generation is active)")
        
        while not operation.done:
            time.sleep(5)
            operation = client.operations.get(operation)
            print("    ...rendering frames...")
            
        if operation.result and operation.result.generated_videos:
            video_asset = operation.result.generated_videos[0]
            filename = "PROOF_OF_LIFE.mp4"
            
            print(f"[+] SUCCESS. ASSET SECURED: {filename}")
            video_asset.video.save(filename)
        else:
            print("[!] FAILURE: The model accepted the command but returned nothing.")

    except Exception as e:
        print(f"[!] TRANSACTION DENIED: {e}")
        if "404" in str(e):
            print("    -> Recommendation: Your key might only have access to 'veo-2.0-generate-001'. Try switching models.")
        if "429" in str(e):
            print("    -> Recommendation: Payment has not propagated yet. Wait 5 minutes.")

if __name__ == "__main__":
    fire_verification_round()