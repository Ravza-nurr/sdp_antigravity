import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

# Konfigürasyon
VIDEO_PATH = "cypress/videos/appointment.cy.js.mp4"
OUTPUT_PATH = "narrated_test_video.mp4"
AUDIO_PATH = "narration.mp3"

# Seslendirme Metni
TEXT = (
    "Merhaba. Bu bir otomatik Cypress testidir. "
    "İlk olarak hasta bilgileri forma giriliyor ve kayıt işlemi yapılıyor. "
    "Ardından doktorlar listeleniyor ve uygun bir doktor seçiliyor. "
    "Son olarak randevu tarihi girilip işlem tamamlanıyor. "
    "Test başarıyla geçti."
)

def main():
    # 1. Video Kontrolü
    if not os.path.exists(VIDEO_PATH):
        print(f"HATA: '{VIDEO_PATH}' bulunamadı.")
        print("Lütfen önce şu komutla testi çalıştırın: npx cypress run --config video=true,supportFile=false")
        return

    print("1. Ses dosyası oluşturuluyor (Google TTS)...")
    try:
        tts = gTTS(TEXT, lang='tr')
        tts.save(AUDIO_PATH)
    except Exception as e:
        print(f"Ses oluşturma hatası: {e}")
        return

    print("2. Video ve ses birleştiriliyor...")
    try:
        video = VideoFileClip(VIDEO_PATH)
        audio = AudioFileClip(AUDIO_PATH)

        # Ses videodan uzunsa videoyu dondurarak uzatmak gerekir ama şimdilik basit tutuyoruz.
        # Eğer video sesden kısaysa ses kesilebilir, bu yüzden testi uzun tuttuk.
        
        final_video = video.set_audio(audio)
        final_video.write_videofile(OUTPUT_PATH, codec='libx264', audio_codec='aac')
        
        print(f"\nBAŞARILI! Videonuz hazır: {os.path.abspath(OUTPUT_PATH)}")
        
        # Temizlik
        if os.path.exists(AUDIO_PATH):
            os.remove(AUDIO_PATH)
            
    except Exception as e:
        print(f"Video işleme hatası: {e}")

if __name__ == "__main__":
    main()
