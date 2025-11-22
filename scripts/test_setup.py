import requests
from moviepy.editor import TextClip
from moviepy.config import get_setting

# 1. Check ElevenLabs API
API_KEY = "sk_108e64f1a75a52af855253b38db033639b645587ff777848"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

print("--- Testing ElevenLabs API ---")
response = requests.post(
    URL,
    json={"text": "Test", "model_id": "eleven_monolingual_v1"},
    headers={"xi-api-key": API_KEY, "Content-Type": "application/json"}
)

if response.status_code == 200:
    print("✅ ElevenLabs API Success! Audio generated.")
else:
    print(f"❌ ElevenLabs API Failed: {response.status_code}")
    print(response.text)

# 2. Check ImageMagick (for Subtitles)
print("\n--- Testing ImageMagick (MoviePy) ---")
try:
    # Check if binary is found
    binary = get_setting("IMAGEMAGICK_BINARY")
    print(f"ImageMagick Binary Path: {binary}")
    
    # Try creating a simple text clip
    clip = TextClip("Test", fontsize=70, color='white')
    print("✅ ImageMagick is working! TextClip created.")
except Exception as e:
    print("❌ ImageMagick Test Failed!")
    print(f"Error: {e}")
    print("Solution: Install ImageMagick and configure MoviePy to point to magick.exe")
