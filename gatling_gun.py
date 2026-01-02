import time
from gemini_brain import get_viral_script
from free_voice import generate_audio
from free_vision import generate_video_file

# CONFIGURATION
TOPICS = [
    "The Dead Internet Theory",
    "AI Self-Replication",
    "The End of Privacy",
    "Neuralink Hacking",
    "Algorithmic Mind Control"
]

def ENGAGE_GATLING_GUN():
    print("--- SYSTEM ONLINE: INDUSTRIAL MODE ---")
    
    for i, topic in enumerate(TOPICS):
        print(f"\n[>>>] CHAMBERING ROUND {i+1}: {topic}")
        
        # 1. Intelligence
        script = get_viral_script(topic)
        print(f"    Script: {script[:40]}...")
        
        # 2. Voice
        audio_path = generate_audio(script, index=i)
        
        # 3. Vision
        video_path = generate_video_file(script, audio_path)
        
        print(f"    [+] ASSET READY: {video_path}")
        
        # Cool down to prevent rate limits
        time.sleep(2)

    print("\n--- BATCH COMPLETE. CHECK YOUR FOLDER. ---")

if __name__ == "__main__":
    ENGAGE_GATLING_GUN()