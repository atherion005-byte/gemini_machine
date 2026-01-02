import google.generativeai as genai
import time
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- DR. X ADAPTIVE CEREBRAL IMPLANT (WITH RETRY) ---
# API key should be provided via environment variable to avoid committing secrets.
API_KEY = os.environ.get("GOOGLE_API_KEY")  # set this in your environment
if not API_KEY:
    logger.warning("GOOGLE_API_KEY not set. Gemini API calls will fail unless set.")

def get_viral_script(topic, retries=3, backoff_factor=2):
    # Read the API key at call time so tests can modify environment variables at runtime.
    api_key = os.environ.get("GOOGLE_API_KEY") or API_KEY
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set. Set environment variable 'GOOGLE_API_KEY' to use Gemini.")
    genai.configure(api_key=api_key)
    
    # We use the text model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    ROLE: You are a viral content strategist.
    TASK: Write a 30-second video script about: {topic}.
    RULES:
    1. Hook (0-3s): Start with a controversial fact.
    2. Body: 3 rapid-fire sentences.
    3. Loop: The last sentence must lead back into the first.
    4. Output: JUST the spoken text. No bolding.
    """
    
    # RETRY LOGIC: Try `retries` times, using exponential backoff on rate limits
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            clean_text = response.text.replace("*", "").replace("#", "").strip()
            return clean_text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate limit" in err_str.lower() or "Rate" in err_str:
                wait = (backoff_factor ** attempt) * 5
                logger.warning(f"    [!] RATE LIMIT HIT. Cooling down for {wait}s... (Attempt {attempt+1}/{retries})")
                time.sleep(wait)
                continue
            else:
                logger.exception("NEURAL FAILURE")
                return "System Error. The AI refused to speak."
    
    logger.error("Rate limit exceeded after %s attempts", retries)
    return "System Error. Rate Limit Exceeded."


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test gemini_brain.get_viral_script")
    parser.add_argument("topic", nargs="?", default="Artificial Intelligence")
    args = parser.parse_args()
    try:
        script = get_viral_script(args.topic)
        print("Generated script:\n", script)
    except Exception as e:
        logger.exception("Failed to generate script")
        print("Error generating script:", e)
