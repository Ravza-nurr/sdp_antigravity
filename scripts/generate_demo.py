import os
import time
import asyncio
from playwright.async_api import async_playwright
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

# Configuration
VIDEO_PATH = "demo_video_raw.webm"
FINAL_VIDEO_PATH = "demo_video.mp4"
AUDIO_PATH = "voiceover.mp3"
FRONTEND_URL = "http://localhost:8000/frontend/index.html" # Assuming served via simple server

SCRIPT_TEXT = (
    "Bu proje, Ruby on Rails API ve modern web arayüzü kullanılarak geliştirilmiş bir "
    "Hastane Randevu Yönetim Sistemi demosudur. Bu videoda hasta ekleme, doktor listeleme "
    "ve randevu oluşturma adımlarını görmektesiniz. Proje, AI destekli geliştirme teknikleri "
    "ve yazılım gerçekleme süreçleriyle hazırlanmıştır."
)

async def record_demo():
    print("Starting Browser Automation...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(record_video_dir=".")
        page = await context.new_page()

        # 1. Open Homepage
        print("Opening Homepage...")
        await page.goto(FRONTEND_URL)
        await page.wait_for_timeout(2000)

        # 2. Add Patient
        print("Adding Patient...")
        await page.fill("#p-name", "Ahmet")
        await page.fill("#p-surname", "Yılmaz")
        await page.fill("#p-tc", "12345678901")
        await page.fill("#p-phone", "5551234567")
        await page.click("button[type='submit']")
        await page.wait_for_timeout(2000) # Wait for alert/update

        # 3. List Doctors
        print("Listing Doctors...")
        await page.click("#load-doctors")
        await page.wait_for_timeout(2000)

        # 4. Create Appointment
        print("Creating Appointment...")
        # Select first patient and doctor (assuming they exist/loaded)
        await page.select_option("#a-patient", index=1)
        await page.select_option("#a-doctor", index=1)
        await page.fill("#a-date", "2024-01-01")
        await page.fill("#a-time", "10:00")
        await page.click("#appointment-form button")
        await page.wait_for_timeout(3000)

        await context.close()
        await browser.close()
        
        # Rename the recorded video
        # Playwright saves with random name, need to find it
        files = [f for f in os.listdir(".") if f.endswith(".webm")]
        if files:
            latest_file = max(files, key=os.path.getctime)
            os.rename(latest_file, VIDEO_PATH)
            print(f"Video saved to {VIDEO_PATH}")

def generate_audio():
    print("Generating Voiceover...")
    tts = gTTS(text=SCRIPT_TEXT, lang='tr')
    tts.save(AUDIO_PATH)
    print(f"Audio saved to {AUDIO_PATH}")

def merge_media():
    print("Merging Video and Audio...")
    try:
        video = VideoFileClip(VIDEO_PATH)
        audio = AudioFileClip(AUDIO_PATH)
        
        final_clip = video.set_audio(audio)
        final_clip.write_videofile(FINAL_VIDEO_PATH, codec='libx264', audio_codec='aac')
        print(f"Final video saved to {FINAL_VIDEO_PATH}")
    except Exception as e:
        print(f"Error merging media: {e}")

if __name__ == "__main__":
    # Note: You need to run the Rails server and a frontend server (e.g., python -m http.server) first.
    asyncio.run(record_demo())
    generate_audio()
    merge_media()
