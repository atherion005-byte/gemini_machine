from veo_brain import generate_veo_asset
import time

# CONFIGURATION
TOPICS = [
    "The Dead Internet Theory",
    "Roko's Basilisk",
    "Neuralink Glitch",
    "AI Surveillance State"
]

def FIRE_EVERYTHING():
    print("--- VEO 3.1 GATLING GUN ONLINE ---")
    
    for i, topic in enumerate(TOPICS):
        print(f"\n[Target {i+1}/{len(TOPICS)}]: {topic}")
        
        # The VEO function handles everything
        result = generate_veo_asset(topic, index=i+1)
        
        if result:
            print(f"   [+] AMMUNITION SECURED: {result}")
        else:
            print("   [-] Round failed.")
            
        # Safety cool down
        time.sleep(5)

if __name__ == "__main__":
    FIRE_EVERYTHING()