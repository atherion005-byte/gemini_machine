import requests
import random
import os

# --- DR. X STOCKPILE PROTOCOL ---
# GET KEY: https://www.pexels.com/api/
PEXELS_API_KEY = "o68RLFaSy9H1LpB80Rn52SezdAmE6BrwZVLvPYGbSum5eSsjFqxJJEiQ" 

def get_cinematic_stock(topic, index=0):
    print(f"    [>>>] HUNTING STOCK FOOTAGE FOR: '{topic}'")
    
    headers = {"Authorization": PEXELS_API_KEY}
    # We force "Dark", "Vertical" to fit the aesthetic
    query = f"{topic} dark abstract technology"
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10&orientation=portrait&size=medium"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'videos' in data and len(data['videos']) > 0:
            # Randomize selection so you don't get the same video twice
            video_data = random.choice(data['videos'])
            video_files = video_data['video_files']
            
            # Find a high-quality MP4 that isn't too heavy
            best_link = None
            for v in video_files:
                if v['file_type'] == 'video/mp4' and v['width'] < 2500:
                    best_link = v['link']
                    break
            
            if not best_link: best_link = video_files[0]['link']
                
            print("    [1] Extracting asset from Pexels Archive...")
            r = requests.get(best_link)
            filename = f"STOCK_BG_{index}.mp4"
            with open(filename, 'wb') as f:
                f.write(r.content)
                
            print(f"    [+] Asset Secured: {filename}")
            return filename
        else:
            print("    [!] PEXELS EMPTY: No footage found.")
            return None

    except Exception as e:
        print(f"    [!] DOWNLOAD ERROR: {e}")
        return None