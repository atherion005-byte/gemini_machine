from gemini_brain import get_viral_script
from free_voice import generate_audio
from free_vision import generate_video_file
from pytrends.request import TrendReq

def IGNITION():
    print("--- SYSTEM ONLINE: DR. X PROTOCOL ---")
    
    # 1. SCANNING
    print("[1] Scanning Global Trends...")
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_df = pytrends.realtime_trending_searches(pn='US')
        topic = trending_df.iloc[0,0]
        print(f"    TARGET LOCKED: {topic}")
    except:
        topic = "Artificial Intelligence"
        print(f"    SCAN BLOCKED. USING FALLBACK: {topic}")

    # 2. INTELLIGENCE
    print("[2] Engaging Gemini Brain...")
    script = get_viral_script(topic)
    print(f"    SCRIPT GENERATED: {script[:30]}...")

    # 3. VOICE
    print("[3] Synthesizing Audio...")
    audio_path = generate_audio(script)

    # 4. VISION
    print("[4] Rendering Video...")
    final_file = generate_video_file(script, audio_path)
    
    print(f"--- SUCCESS. FILE READY: {final_file} ---")

if __name__ == "__main__":
    IGNITION()