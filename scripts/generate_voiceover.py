import os
import numpy as np
import requests
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, ImageClip, vfx
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
ELEVENLABS_API_KEY = "f0e2bdbab499ce82cc5ab7641783aa51cb118e594bef3e8d5b8ea7be03e73e2c"
VOICE_ID = "lxZLq5dcyw12UangGJgN" # Requested Voice ID
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

# Input/Output Paths
VIDEO_PATH = "cypress/videos/appointment.cy.js.mp4" 
OUTPUT_VIDEO_PATH = "final_test_voiceover.mp4"
AUDIO_OUTPUT_DIR = "temp_audio"
TARGET_DURATION = 35.0

# Timeline Data (Time in seconds - Original)
TIMELINE = [
    {"time": 0.5, "text": "Test başlatıldı."},
    {"time": 2.1, "text": "Giriş yapılıyor."},
    {"time": 5.8, "text": "Giriş başarılı."},
    {"time": 9.3, "text": "Kayıt formu açıldı."},
    {"time": 12.0, "text": "Kayıt işlemi tamamlandı."}
]

def generate_audio(text, index):
    """
    Generates audio using ElevenLabs API. Falls back to gTTS if it fails.
    """
    print(f"Generating audio for: '{text}' with ElevenLabs...")
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2", # Better for Turkish
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        
        if response.status_code == 200:
            filename = os.path.join(AUDIO_OUTPUT_DIR, f"clip_{index}.mp3")
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            print(f"ElevenLabs Error ({response.status_code}): {response.text}")
            print("Falling back to Google TTS...")
            return generate_audio_gtts(text, index)
            
    except Exception as e:
        print(f"Error calling ElevenLabs: {e}")
        return generate_audio_gtts(text, index)

def generate_audio_gtts(text, index):
    """
    Fallback: Generates audio using Google TTS (gTTS).
    """
    try:
        tts = gTTS(text=text, lang='tr')
        filename = os.path.join(AUDIO_OUTPUT_DIR, f"clip_{index}_gtts.mp3")
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating gTTS audio: {e}")
        return None

def create_subtitle_clip(text, duration, fontsize=30):
    """
    Creates a MoviePy ImageClip for the subtitle using Pillow (No ImageMagick required).
    """
    # Image settings
    width, height = 1280, 100  # Subtitle strip size
    bg_color = (0, 0, 0, 180)  # Semi-transparent black
    text_color = (255, 255, 255, 255) # White

    # Create image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load font (Try Arial, fallback to default)
    try:
        font = ImageFont.truetype("arial.ttf", fontsize)
    except IOError:
        font = ImageFont.load_default()
        print("Warning: Arial font not found, using default.")

    # Calculate text position to center it
    # getbbox returns (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Draw background rectangle for better readability
    padding = 10
    draw.rectangle(
        [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
        fill=bg_color
    )
    
    # Draw text
    draw.text((x, y), text, font=font, fill=text_color)

    # Convert to numpy array for MoviePy
    img_np = np.array(img)
    
    # Create ImageClip
    clip = ImageClip(img_np).set_duration(duration)
    # Position at the bottom of the screen
    clip = clip.set_position(('center', 'bottom'))
    
    return clip

def process_video():
    """
    Main function to process the video:
    1. Stretch video to TARGET_DURATION.
    2. Scale timeline timestamps.
    3. Generate audio and subtitles.
    4. Export.
    """
    # Ensure temp directory exists
    if not os.path.exists(AUDIO_OUTPUT_DIR):
        os.makedirs(AUDIO_OUTPUT_DIR)

    # Load Video
    try:
        video = VideoFileClip(VIDEO_PATH)
    except OSError:
        print(f"Error: Could not find video at {VIDEO_PATH}. Please check the path.")
        return

    # Calculate Speed Factor
    original_duration = video.duration
    print(f"Original Duration: {original_duration}s")
    
    if original_duration < TARGET_DURATION:
        speed_factor = original_duration / TARGET_DURATION
        print(f"Slowing down video by factor {speed_factor:.2f} to reach {TARGET_DURATION}s")
        video = video.fx(vfx.speedx, speed_factor)
        time_scale = TARGET_DURATION / original_duration
    else:
        time_scale = 1.0

    audio_clips = []
    subtitle_clips = []
    
    # Process each timeline item
    for i, item in enumerate(TIMELINE):
        text = item["text"]
        # Scale timestamp
        start_time = item["time"] * time_scale
        print(f"Timestamp for '{text}': {item['time']}s -> {start_time:.2f}s")

        # 1. Generate Audio
        audio_file = generate_audio(text, i)
        
        if audio_file:
            # Load the generated audio
            audio_clip = AudioFileClip(audio_file)
            # Set the start time in the video
            audio_clip = audio_clip.set_start(start_time)
            audio_clips.append(audio_clip)

            # 2. Create Subtitle (Custom Pillow Function)
            # Duration is audio length + 0.5s buffer
            sub_duration = audio_clip.duration + 0.5
            subtitle = create_subtitle_clip(text, sub_duration)
            subtitle = subtitle.set_start(start_time)
            subtitle_clips.append(subtitle)

    # 3. Composite Audio
    if video.audio:
        original_audio = video.audio.volumex(0.1)
        if audio_clips:
            final_audio = CompositeAudioClip([original_audio] + audio_clips)
        else:
            final_audio = original_audio
    else:
        final_audio = CompositeAudioClip(audio_clips) if audio_clips else None

    # 4. Composite Video (With Subtitles)
    # Overlay subtitles on top of the video
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    if final_audio:
        final_video.audio = final_audio

    # 5. Export
    print("Rendering final video...")
    final_video.write_videofile(OUTPUT_VIDEO_PATH, codec="libx264", audio_codec="aac")
    print(f"Done! Saved to {OUTPUT_VIDEO_PATH}")

if __name__ == "__main__":
    process_video()
