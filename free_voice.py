from gtts import gTTS

def generate_audio(text_content, index=0):
    print("    [+] Synthesizing vocal patterns...")
    filename = f"temp_audio_{index}.mp3"
    tts = gTTS(text=text_content, lang='en', tld='co.uk') 
    tts.save(filename)
    return filename