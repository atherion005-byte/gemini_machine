from google import genai
import os

# --- DR. X INVENTORY SCAN ---
API_KEY = "AIzaSyCA-gkmoVfyiizE2cwgFT5xRTAtws525FU"

client = genai.Client(api_key=API_KEY)

print("--- SCANNING GOOGLE ARMORY ---")
try:
    count = 0
    # List all models available to your key
    for m in client.models.list():
        # We are looking for "veo" or "video" capabilities
        if "veo" in m.name.lower() or "video" in m.name.lower():
            print(f" [!!!] VIDEO WEAPON FOUND: {m.name}")
            print(f"       Capabilities: {m.supported_generation_methods}")
            count += 1
        elif "gemini" in m.name.lower() and "flash" in m.name.lower():
             # Just to confirm your text brain is still there
             print(f" [+] Text/Multimodal Model: {m.name}")
    
    if count == 0:
        print("\n[!] CRITICAL: No 'Veo' or 'Video' models found in your account.")
        print("    This means you are not whitelisted for the Video API yet.")
        print("    You may need to apply for Trusted Tester access.")

except Exception as e:
    print(f"SCAN FAILED: {e}")